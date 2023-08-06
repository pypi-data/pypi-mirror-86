# Utility to query and set temps via Ethernet on Meerstetter
from __future__ import absolute_import, unicode_literals, print_function, division
import socket
import random
import six
import struct
import threading
import logging

from ..testing.sensors import SensorEmulator

DEFAULT_TIMEOUT = 5
TEC_CURRENT_LIMIT = 10.7


error_codes = {
    '+01': 'Command not available',
    '+02': 'Device is busy',
    '+03': 'Communication error',
    '+04': 'Format error',
    '+05': 'Parameter not available',
    '+06': 'Parameter is read only',
    '+07': 'Value is out of range',
    '+08': 'Instance not available'
}

STATUS_CODES = {
    0: 'init', 1: 'ready', 2: 'run', 3: 'error',
    4: 'bootloader', 5: 'resetting'
}


def hex_to_int(hexstring):
    return int(hexstring, 16)


def hex_to_float32(hexstring):
    try:
        if six.PY2:
            byteval = hexstring.strip().decode('hex')
        else:
            byteval = bytes.fromhex(hexstring.strip())
    except Exception as err:
        raise RuntimeError('cannot decode string {}!\n{}'.format(hexstring, err))
    return struct.unpack(str('!f'), byteval)[0]


def float32_to_hex(f):
    return format(struct.unpack(str('<I'), struct.pack(str('<f'), f))[0], 'X')


class CRCCalculator(object):
    def __init__(self):
        self.polynomial = 0x1021
        self.preset = 0
        self._lut = [self._calc_initial(i) for i in range(256)]

    def _calc_initial(self, c):
        crc = 0
        c = c << 8
        for j in range(8):
            if (crc ^ c) & 0x8000:
                crc = (crc << 1) ^ self.polynomial
            else:
                crc = crc << 1
            c = c << 1
        return crc

    def _update_crc(self, crc, c):
        cc = 0xff & c

        tmp = (crc >> 8) ^ cc
        crc = (crc << 8) ^ self._lut[tmp & 0xff]
        crc = crc & 0xffff
        return crc

    def __call__(self, msg):
        crc = self.preset
        for c in msg:
            crc = self._update_crc(crc, ord(c))
        return format(crc, '0>4X')


class MeerstetterTEC1090Emulator(object):
    def __init__(self, address, port):
        self._heatsinks = {i: SensorEmulator(38, 0.1, 0.001) for i in range(1, 4)}
        self._currents = {i: SensorEmulator(8, 0.1, 0.001) for i in range(1, 4)}
        self._temperatures = {i: SensorEmulator(-90, 0.1, 0.01) for i in range(1, 4)}

    def disconnect(self):
        pass

    def connect(self):
        pass

    def get_status(self, addr):
        return 2

    def get_heatsink_temp(self, addr):
        return self._heatsinks[addr].current_value

    def set_ccd_temp(self, addr, val):
        self._temperatures[addr].target_value = val

    def get_ccd_temp(self, addr):
        return self._temperatures[addr].current_value

    def get_setpoint(self, addr):
        return self._temperatures[addr].target_value

    def get_current(self, addr):
        return self._currents[addr].current_value


class MeerstetterTEC1090(object):
    """
    Class to use TCP/IP to communicate with TEC-1090 controllers
    mounted in LTR-1200. Communication protocol is MeCom.

    See MeCom protocol spec document 5117B and TEC protocol document
    5136 for details.
    """
    def __init__(self, address, port):

        self.logger = logging.getLogger('meerstetter.{}'.format(address))
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('meerstetter.log')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.address = address
        self.port = port
        self.seq_no = random.randint(1, 1000)
        self.crc_calc = CRCCalculator()
        self.tec_current_limit = TEC_CURRENT_LIMIT
        self._lock = threading.Lock()
        self.sock = None

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.sock.close()
        self.sock = None

    def connect(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(DEFAULT_TIMEOUT)
            s.connect((self.address, self.port))
            welcome = s.recv(1024)
            if 'Welcome' not in welcome.decode():
                self.logger.error('did not receive welcome message from meerstetter')
                raise IOError('did not receive welcome message from meerstetter')
        except Exception:
            # connection failed
            return False
        self.sock = s
        return True

    def _assemble_frame(self, address, payload):
        """
        Assemble the frame of data to send.

        Transmissions are sent in blocks of data known as frames. Each frame has
        several fields:

        1: Control (source); ASCII Char; 1 bytes
        2: Address; UINT8; 2 bytes
        3: Sequence No; UINT16; 4 bytes
        4: Payload; N bytes
        5: Checksum, 4 bytes
        6: End of Frame, 1 byte <CR>
        """
        cs = '#'
        addr = format(address, '0>2X')
        seq = format(self.seq_no, '0>4X')
        self.seq_no += 1
        msg = cs + addr + seq + payload
        eof = '\r'
        return msg + self.crc_calc(msg) + eof

    def _send_frame(self, frame_msg):
        # threadsafe and error-safe opening of socket
        with self._lock:
            self.sock.send(frame_msg.encode())
            ret_msg = self.sock.recv(1024)
        ret_msg = ret_msg.decode().strip()
        self.logger.info('got ret_msg = {}'.format(ret_msg))
        self._check_response(frame_msg, ret_msg)
        return self._strip_response(ret_msg)

    def _check_response(self, frame_msg, ret_msg):
        if ret_msg[0] == '!' and frame_msg[1:7] == ret_msg[1:7]:
            # a valid response, and same seq no. so far so good
            crc_back = ret_msg[-4:]
            crc_out = frame_msg[-5:-1]
            package_in = ret_msg[:-4]
            if self.crc_calc(package_in) != crc_back and crc_out != crc_back:
                raise IOError('checksum of return message not OK:\nOut: {}\nBack: {}'.format(
                                frame_msg, ret_msg
                              ))
        else:
            raise IOError('response not from device, or sequence number mismatch:\nOut: {}\nBack: {}'.format(
                            frame_msg, ret_msg
                          ))

    def _strip_response(self, ret_msg):
        return ret_msg[7:-4]

    def get_param(self, address, param_no, instance, param_type='float'):
        payload = '?VR{param_no:0>4X}{instance:0>2X}'.format(
            param_no=param_no, instance=instance
        )
        self.logger.info('payload = {}'.format(payload))
        frame_msg = self._assemble_frame(address, payload)
        encoded_param_val = self._send_frame(frame_msg)
        if encoded_param_val == '+05':
            raise IOError('param {} not available'.format(param_no))

        if encoded_param_val in error_codes:
            raise IOError(
                'failed to get param {}\n{}'.format(param_no, error_codes[encoded_param_val])
            )

        if param_type == 'float':
            return hex_to_float32(encoded_param_val)
        else:
            return hex_to_int(encoded_param_val)

    def reset_tec(self, address):
        payload = 'RS'
        frame_msg = self._assemble_frame(address, payload)
        ret_msg = self._send_frame(frame_msg)
        if ret_msg != '':
            raise IOError('unexpected response to reset command {}'.format(ret_msg))

    def set_ccd_temp(self, address, target_temp):
        param_no = 3000
        payload = 'VS{param_no:0>4X}{instance:0>2X}{encoded_val}'.format(
            param_no=param_no, instance=1,
            encoded_val=float32_to_hex(target_temp)
        )
        frame_msg = self._assemble_frame(address, payload)
        ret_msg = self._send_frame(frame_msg)
        if ret_msg.startswith('+'):
            if ret_msg in error_codes:
                raise IOError(error_codes[ret_msg])
            else:
                raise IOError('unknown error code {}'.format(ret_msg))

    def get_ccd_temp(self, address):
        self.logger.info('getting CCD{} temp'.format(address))
        param_no = 1000
        return self.get_param(address, param_no, 1)

    def get_setpoint(self, address):
        param_no = 1010
        return self.get_param(address, param_no, 1)

    def get_heatsink_temp(self, address):
        param_no = 1001
        return self.get_param(address, param_no, 1)

    def get_power(self, address):
        current = self.get_param(address, 1020, 1)
        voltage = self.get_param(address, 1021, 1)
        return current*voltage

    def get_current(self, address):
        return self.get_param(address, 1020, 1)

    def get_status(self, address):
        param_no = 104
        status = self.get_param(address, param_no, 1, param_type='int')
        return status
