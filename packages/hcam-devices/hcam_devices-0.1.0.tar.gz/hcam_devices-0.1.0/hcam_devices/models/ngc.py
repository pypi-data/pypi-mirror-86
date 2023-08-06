import os
import time
import six

from astropy.io import ascii
from astropy.io import fits
from astropy.time import Time
from twisted.logger import Logger

from ..utils.obsmodes import Idle, get_obsmode
from ..devices.ngc import (NGCDevice, NGCEmulator)
from ..machines import create_machine

if not six.PY3:
    from StringIO import StringIO
else:
    from io import StringIO


class NGC(object):
    """
    Model for an ESO NGC controller
    """
    log = Logger()

    settable_attributes = ()
    extra_rpc_calls = ('start', 'stop', 'abort', 'pon', 'poff',
                       'seq_start', 'seq_stop', 'trigger', 'reset',
                       'summary', 'status', 'setup',
                       'load_setup', 'add_hdu', 'cmd')

    def __init__(self, emulate=True):
        if emulate:
            self._dev = NGCEmulator()
        else:
            self._dev = NGCDevice()

        self._server = create_machine('ngc_sw', initial_context={'device': self})
        self.machines = {'ngc_server': self._server}

    def on_load(self):
        """
        Run commands necessary to bring up the NGC controller

        Called by state machine on transitions to LOADED state
        """
        try:
            output = self._dev.start_ngc_sw()
        except Exception as e:
            self.log.error('could not start NGC software: ' + str(e))
            return False

        for key in output:
            msg = output[key]
            self.log.info("cmd {}: {}".format(key, msg))
        return True

    def on_standby(self):
        """
        Load HiPERCAM specific settings

        Called by state machine on transitions to STANDBY state
        """
        try:
            output = self._dev.setup_ngc_hipercam()
        except Exception as e:
            self.log.error('could not setup NGC for hipercam: ' + str(e))
            return False

        for key in output:
            msg = output[key]
            self.log.info("cmd {}: {}".format(key, msg))
        return True

    def cmd(self, cmd, *args):
        try:
            msg, cmd_ok = self._dev.send_command(cmd, *args)
            if not cmd_ok:
                self.log('cmd {} failed with msg {}'.format(cmd, msg))
        except Exception as e:
            msg = 'could not run command {}: {}'.format(cmd, e)
            self.log.error('could not run command {}: {}'.format(cmd, e))
            cmd_ok = False

        return msg, cmd_ok

    def telemetry(self):
        """
        Called periodically to provide status etc for the NGC
        """
        ts = Time.now()
        tel = dict(
            timestamp=ts,
            state={key: self.machines[key].configuration for key in self.machines})
        tel.update(self._dev.database_summary)
        frame_no, ok = self._dev.send_command('status', 'DET.FRAM2.NO')
        if not ok:
            tel['exposure.frame'] = 0
        else:
            tel['exposure.frame'] = frame_no
        return tel

    def start(self, *args):
        return self.cmd('start')

    def stop(self, *args):
        return self.cmd('stop')

    def abort(self, *args):
        return self.cmd('abort')

    def pon(self, *args):
        return self.cmd('cldc 0 enable')

    def poff(self, *args):
        return self.cmd('cldc 0 disable')

    def seq_start(self, *args):
        return self.cmd('seq 0 start')

    def seq_stop(self, *args):
        return self.cmd('seq 0 stop')

    def trigger(self, *args):
        return self.cmd('trigger')

    def reset(self, *args):
        return self.cmd('reset')

    def summary(self, *args):
        return self._dev.database_summary

    def status(self, param_name=None):
        if param_name is None:
            return self.cmd('status')

        response, response_ok = self.cmd('status', param_name)
        if not response_ok:
            return response, response_ok

        try:
            name, val = response.split()
            if name != param_name:
                msg = 'unexpected response: {} vs {}'.format(
                    name, param_name
                )
                return msg, False

            return val, response_ok
        except Exception as err:
            return str(err), False

        return self.cmd('status', param_name)

    def setup(self, param_name, value):
        return self.cmd('setup', param_name, value)

    def load_setup(self, data):
        """
        Post a JSON setup to the server

        Parameters
        -----------
        data : dict
            setup info
        """
        try:
            obsmode = get_obsmode(data)
        except Exception:
            return False, 'could not parse obsmode data'

        resp = self.cmd('seq stop')
        if not resp:
            self.log.error('could not stop sequencer')
            return False, 'could not stop sequencer'

        time.sleep(0.1)
        resp = self.cmd(obsmode.readmode_command)
        if not resp:
            self.log.error('could not set read mode: ' + resp)
            return False, 'could not set read mode: ' + resp

        time.sleep(0.1)
        resp = self.cmd(obsmode.acq_command)
        if not resp:
            self.log.error('could not start acquisition process: ' + resp)
            return False, 'could not start acquisition process: ' + resp

        time.sleep(0.1)
        for header_command in obsmode.header_commands:
            resp = self.cmd(header_command)
        if not resp:
            msg = 'could not set header param {}: {} '.format(
                header_command, resp
            )
            self.log.error(msg)
            return False, msg

        time.sleep(0.1)
        resp = self.cmd(obsmode.setup_command)
        if not resp:
            self.log.error('could not setup run: ' + resp)
            return False, 'could not setup run: ' + resp

        if isinstance(obsmode, Idle):
            """
            A run start will start the sequencer, saving data and clearing the chips.
            There is no run start when we switch to idle mode, so start the sequencer
            manually
            """
            resp = self.cmd('seq start')
            if not resp:
                self.log.error('could not start sequencer: ' + resp)
                return False, 'could not start sequencer: ' + resp

        return True, 'All OK'

    def add_hdu(self, table_data, run_number):
        """
        Handle an uploaded table, and append it to the appropriate FITS file

        Parameters
        -----------
        table_data: bytes
            a binary encoded VOTable, which we will write to a FITS HDU,
            which is appended onto the original FITS file.
        run_number: int
            the run to append the table data to
        """
        try:
            table_data = StringIO(table_data)
            t = ascii.read(table_data, format='ecsv')
        except Exception as e:
            self.log.error('cannot decode table data: ' + str(e))
            return

        filename = os.path.join('/data', "run{:04d}.fits".format(run_number))
        if not os.path.exists(filename):
            self.log.error('no such filename exists: ' + filename)
            return

        try:
            new_hdu = fits.table_to_hdu(t)
            existing_hdu_list = fits.open(
                filename, mode='append', memmap=True
            )
            existing_hdu_list.append(new_hdu)
            existing_hdu_list.flush()
        except Exception as e:
            self.log.error('could not write HDU to run: ' + str(e))
