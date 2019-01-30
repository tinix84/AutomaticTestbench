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

DEFAULT_TIMEOUT = 1

class E3631A(object):
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

    def set_all_output_on(self):
        """Switch on all the output channel"""
        cmd='OUTP ON'
        self.port.write_string(cmd)

    def set_all_output_off(self):
        """Switch off all the output channel"""
        cmd='OUTP OFF'
        self.port.write_string(cmd)
        
    def set_P6Vchannel_voltage_current(self, voltage_value, current_value):
        """Specify voltage and current for 6V channel"""
        #APPLy {P6V | P25V | N25V}[,{<voltage>| DEF | MIN | MAX}[,{<current>| DEF | MIN | MAX}]]
        cmd='APPL P6V, %s, %s' % (str(voltage_value), str(current_value))
        self.port.write_string(cmd)

    def set_P25Vchannel_voltage_current(self, voltage_value, current_value):
        """Specify voltage and current for positive 25V channel"""
        #APPLy {P6V | P25V | N25V}[,{<voltage>| DEF | MIN | MAX}[,{<current>| DEF | MIN | MAX}]]
        cmd='APPL P25V, %s, %s' % (str(voltage_value), str(current_value))
        self.port.write_string(cmd)

    def set_N25Vchannel_voltage_current(self, voltage_value, current_value):
        """Specify voltage and current for negative 25V channel"""
         #APPLy {P6V | P25V | N25V}[,{<voltage>| DEF | MIN | MAX}[,{<current>| DEF | MIN | MAX}]]
        cmd='APPL N25V, %s, %s' % (str(voltage_value), str(current_value))
        self.port.write_string(cmd)

    def get_P6Vchannel_measure_voltage(self):
        """Query the output voltage for +6V output"""
        #MEASure[:VOLTage][:DC]? [{P6V | P25V | N25V}]
        cmd='MEAS:VOLT? P6V'
        value_str = self.port.query(cmd)
        return value_str
        
    def get_P25Vchannel_measure_voltage(self):
        """Query the output voltage for +25V output""" 
        #MEASure[:VOLTage][:DC]? [{P6V | P25V | N25V}]
        cmd='MEAS:VOLT? P25V'
        value_str = self.port.query(cmd)
        return value_str
    
    def get_N25Vchannel_measure_voltage(self):
        """Query the output voltage for -25V output""" 
        #"MEASure[:VOLTage][:DC]? [{P6V | P25V | N25V}]
        cmd='MEAS:VOLT? N25V'
        value_str = self.port.query(cmd)
        return value_str
        
    def get_P6Vchannel_measure_current(self):
        """Query the output voltage for +6V output"""
        #MEASure:CURRent[:DC]? [{P6V | P25V | N25V}]
        cmd='MEAS:CURR? P6V'
        value_str = self.port.query(cmd)
        return value_str
        
    def get_P25Vchannel_measure_current(self):
        """Query the output voltage for +25V output""" 
        #MEASure:CURRent[:DC]? [{P6V | P25V | N25V}]
        cmd='MEAS:CURR? P25V'
        value_str = self.port.query(cmd)
        return value_str
    
    def get_N25Vchannel_measure_current(self):
        """Query the output voltage for -25V output""" 
        #MEASure:CURRent[:DC]? [{P6V | P25V | N25V}]
        cmd='MEAS:CURR? N25V'
        value_str = self.port.query(cmd)
        return value_str
                
    def trigger(self):
        """Trigger signal to execute a command"""
        self.port.write_string("*TRG")


if __name__ == "__main__":

    psupply_board = 0
    psupply_address = 2
    psupply_protocol = 'GPIB'

    gen_port = generic_port.PyVisaPort(psupply_protocol, psupply_address, psupply_board, timeout = DEFAULT_TIMEOUT)
    psu = E3631A(gen_port, DEFAULT_TIMEOUT)
    psu.connect()
    print "  --> gen id: `%s'" % psu.identify()
    psu.reset()
    time.sleep(1)
    psu.set_P6Vchannel_voltage_current(1.1, 0.1)
    psu.set_all_output_on()
    print "  --> out voltage: `%s'" % psu.get_P6Vchannel_measure_voltage()
    print "  --> out current: `%s'" % psu.get_P6Vchannel_measure_current()
    time.sleep(3)  
    psu.set_all_output_off()    
    psu.disconnect()

    print "Done"
