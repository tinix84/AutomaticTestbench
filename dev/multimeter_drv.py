# -*- coding: utf-8 -*-
"""@package docstring
Documentation for this module.

More details.
"""
import sys
sys.path.append('../include/')
import time
import generic_port
import debug_msg
import numpy as np

DEFAULT_TIMEOUT = 1

class HP34401A(object):
    """Documentation for a class.

    Represents a Agilent E3631A triple out power supply.
    """

    def __init__(self, port_obj, timeout = DEFAULT_TIMEOUT):
        """The constructor."""
        self.port = port_obj
        self.timout = timeout

    def is_usb(self):
        """TBD. Check if the connection is USB."""
        print debug_msg.TBD_MSG
        
    def is_serial(self):
        """TBD. Check if the connection is serial."""
        print debug_msg.TBD_MSG

    def is_gpib(self):
        """TBD. Check if the connection is GPIB."""
        print debug_msg.TBD_MSG

    def is_connected(self):
        """TBD. Check if the connection is established."""
        print debug_msg.TBD_MSG

    def connect(self):
        """Connect to the gen."""
        self.port.open_stream()

    def disconnect(self):
        """Disconnect if connected."""
        self.port.close_stream()

    def identify(self):
        """Ask the gen for its ID."""
        return self.port.query("*IDN?",1000)

    def reset(self):
        """Reset the instrument to default setting."""
        return self.port.write_string('*RST;*CLS' )

    def query_options(self):
        """Query the gen options."""
        return self.query("*OPT?")
        
    def set_voltage_mode(self, voltage_value):
        """set the correct voltage range for a given value"""
        #CONFigure:<function> {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
        fs = np.ceil(voltage_value)
        rs = 10**(np.ceil(np.log(fs)/np.log(10))-6)
        cmd='CONF:VOLT:DC %d, %f' % (fs, rs)
        self.port.write_string(cmd)

    def set_current_mode(self, current_range, resolution):
        """set the correct voltage range for a given value"""
        #CONFigure:<function> {<range>|MIN|MAX|DEF},{<resolution>|MIN|MAX|DEF}
        if current_range == None:
            current_range = 1
        if resolution == None:
            resolution = 10**(np.ceil(np.log(current_range)/np.log(10))-6)
        cmd='CONF:CURR:DC %e, %e' % (current_range, resolution)
        self.port.write_string(cmd)

    def set_trigger_source_bus(self):
        """Switch off all the output channel"""
        #TRIGger:SOURce {BUS|IMMediate|EXTernal}
        cmd='TRIG:SOUR BUS'
        self.port.write_string(cmd)
        
    def set_trigger_source_immediate(self):
        """Switch off all the output channel"""
        #TRIGger:SOURce {BUS|IMMediate|EXTernal}
        cmd='TRIG:SOUR IMM'
        self.port.write_string(cmd)
        
    def set_trigger_source_external(self):
        """Switch off all the output channel"""
        #TRIGger:SOURce {BUS|IMMediate|EXTernal}
        cmd='TRIG:SOUR EXT'
        self.port.write_string(cmd)

    def set_display_off(self):
        """Switch off display"""
        #DISPlay {OFF|ON}
        self.port.write_string("DISP OFF")

    def set_display_on(self):
        """Switch on display"""
        #DISPlay {OFF|ON}
        self.port.write_string("DISP ON")

    def get_measure(self):
        """Measure the value in the actual configuration and send it out"""
        cmd='READ?'
        value_str = self.port.query(cmd)
        return value_str
                
    def trigger(self):
        """Trigger signal to execute a command"""
        self.port.write_string("*TRG")


if __name__ == "__main__":

    dmm_board = 0
    dmm_address = 3
    dmm_protocol = 'GPIB'

    #gen_port = generic_port.PyVisaPort(protocol = dmm_protocol, dmm_address, dmm_board, timeout = DEFAULT_TIMEOUT)
    gen_port = generic_port.PySerialPort(protocol = "SERIAL", port = 14, timeout = DEFAULT_TIMEOUT, baud = 9600)
    dmm = HP34401A(gen_port, DEFAULT_TIMEOUT)
    dmm.connect()
    print "  --> gen id: `%s'" % dmm.identify()
    dmm.reset()
    time.sleep(1)
    dmm.set_voltage_mode(5)
    dmm.set_trigger_source_immediate()
    print "  --> out voltage: `%s'" % dmm.get_measure()
    dmm.disconnect()

    print "Done"
