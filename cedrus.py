from serial.tools import list_ports
from serial import Serial
from psychopy import core
import re

def print_ports():
    ports = list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

def find_port(serial_num):
    '''
    finds port handle with given hardware serial number
    '''
    ports = list_ports.comports()
    target_port = None
    for port, desc, hwid in sorted(ports):
        sn = re.findall('SER=(\w+)', hwid)
        if sn:
            if sn[0] == serial_num:
                target_port = port
                break
    if target_port is None:
        raise Exception('Serial number %s not found!'%serial_num)
    else:
        return target_port

class RBx20:
    '''
    wrapper for Cedrus RB-620 Response Box

    Expects box to be set to ascii protocol (switch 1 in down position
    and switch 2 up). Will throw likely throw error otherwise.

    Last two switches control the baud rate. Make sure hardware and software
    baud rates (as set in __init__) match. If switches 3 & 4 are both down,
    the baud rate is 19200.
    '''
    def __init__(self, serial_num, baudrate = 19200):
        self.port = find_port(serial_num)
        self.ser = Serial(self.port, baudrate = baudrate)
        self.rt_clock = core.Clock()

    def reset(self):
        '''
        Flushes the input buffer and resets the reaction time clock.
        '''
        self.rt_clock.reset()
        self.ser.reset_input_buffer() # flush

    def waitKeys(self, timeout = None, reset = True):
        '''
        Returns key pressed and reaction time (relative to last reset)
        or None, None if times out
        '''
        if reset:
            self.reset()
        self.ser.timeout = timeout # None is no timeout
        press = self.ser.read(1)
        rt = self.rt_clock.getTime()
        if press == b'':
            return None, None
        key = int(press) # ascii character to key number
        return key, rt

    def waitPress(self, **kwargs):
        key, rt = self.waitKeys(**kwargs)
        return key, rt

    def getNext(self):
        '''
        returns whatever is next in the buffer, or None, None if nothing
        '''
        key, rt = self.waitKeys(timeout = 0, reset = False)
        return key, rt

    def close(self):
        self.ser.close()

    def __del__(self):
        self.close()
