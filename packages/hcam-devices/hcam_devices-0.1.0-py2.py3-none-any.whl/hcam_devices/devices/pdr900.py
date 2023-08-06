# Utility to communicate with MKS PDR900 Vacuum Guage via RS232
from __future__ import absolute_import, unicode_literals, print_function, division
import re
import socket
import threading
import six

from astropy.utils.decorators import lazyproperty
from astropy.time import Time, TimeDelta
from astropy.io import ascii

from ..testing.sensors import SensorEmulator

DEFAULT_TIMEOUT = 5  # seconds

# MESSAGES (as strings, don't forget to format and encode)
DOWNLOAD = '@{addr:03d}DL{comm};FF'
SERIAL_NO = '@{addr:03d}SNC{comm};FF'
FIRMWARE = '@{addr:03d}FVC{comm};FF'
ADDRESS = '@{addr:03d}ADC{comm};FF'
DLOG_CTRL = '@{addr:03d}DLC{comm};FF'
DLOG_TIME = '@{addr:03d}DLT{comm};FF'
PRESSURE = '@{addr:03d}PR1{comm};FF'

# rename socket.error
if six.PY2:
    ConnectionRefusedError = socket.error


class VacuumGaugeError(Exception):
    pass


class PDR900Emulator(object):

    def __init__(self, host, port):
        self._sensor = SensorEmulator(1.0e-5, 1.0e-6, 0.0)

    def disconnect(self):
        pass

    def connect(self):
        pass

    @property
    def pressure(self):
        return self._sensor.current_value


class PDR900(object):

    def __init__(self, host, port):
        """
        Creates a PDR900 object for communication over serial.

        Parameters
        -----------
         port : string
            port device representing the vacuum gauge
        """
        self.port = port
        self.host = host
        self.logging_start_time = None
        try:
            self.connect()
        except ConnectionRefusedError:
            self.sock = None
        self._lock = threading.Lock()

    def __del__(self):
        self.close()

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.settimeout(5)
        self.sock = s

    def close(self):
        self.sock.close()
        self.sock = None

    def _parse_response(self, response):
        pattern = '@(.*)ACK(.*);FF'
        result = re.match(pattern, response)
        if result is None:
            raise VacuumGaugeError('could not parse response {}'.format(
                response
            ))
        if len(result.groups()) != 2:
            raise VacuumGaugeError('unexpected result when parsing response {}'.format(
                response
            ))
        return result.groups()

    def _send_recv(self, message, data):
        # try and connect if we are not already
        msg = message.format(**data).encode()
        if self.sock is None:
            try:
                self.connect()
            except ConnectionRefusedError:
                raise VacuumGaugeError('not connected')

        self.sock.send(msg)
        self.sock.settimeout(DEFAULT_TIMEOUT)
        response = self.sock.recv(1024).decode().rstrip('\r\n')
        addr, retval = self._parse_response(response)
        return addr, retval

    @lazyproperty
    def address(self):
        # connect once to find address and hard-code
        data = dict(addr=254, comm='?')
        _, addr = self._send_recv(ADDRESS, data)
        return int(addr)

    @lazyproperty
    def firmware_version(self):
        data = dict(addr=self.address, comm='?')
        _, fwver = self._send_recv(FIRMWARE, data)
        return fwver

    @lazyproperty
    def serial_number(self):
        data = dict(addr=self.address, comm='?')
        _, serno = self._send_recv(SERIAL_NO, data)
        return serno

    @property
    def pressure(self):
        data = dict(addr=self.address, comm='?')
        addr, response = self._send_recv(PRESSURE, data)
        return float(response) / 1000

    def start_logging(self):
        data = dict(addr=self.address, comm='!START')
        addr, response = self._send_recv(DLOG_CTRL, data)
        if response != 'START':
            raise VacuumGaugeError('failed to start logging')
        self.logging_start_time = Time.now()

    def stop_logging(self):
        data = dict(addr=self.address, comm='!STOP')
        addr, response = self._send_recv(DLOG_CTRL, data)
        if response != 'STOP':
            raise VacuumGaugeError('failed to stop logging')
        self.logging_start_time = Time.now()

    def set_log_interval(self, hours, mins, secs):
        assert secs < 60, 'seconds must be less than 60'
        assert mins < 60, 'minutes must be less than 60'
        tstring = '!{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        data = dict(addr=self.address, comm=tstring)
        addr, response = self._send_recv(DLOG_TIME, data)
        if response != tstring[1:]:
            raise VacuumGaugeError('failed to set logging time')

    def get_log_interval(self):
        data = dict(addr=self.address, comm='?')
        addr, response = self._send_recv(DLOG_TIME, data)
        try:
            h, m, s = [float(val) for val in response.split(':')]
        except Exception:
            raise VacuumGaugeError('cannot parse log interval response: ' + response)
        return TimeDelta(3600*h + 60*m + s, format='sec')

    def get_log_data(self):
        data = dict(addr=self.address, comm='?')
        addr, pdata = self._send_recv(DOWNLOAD, data)
        pdata = pdata.rstrip('\x03').replace('\r', '\n')
        return ascii.read(pdata, delimiter=';')
