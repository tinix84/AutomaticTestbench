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

class KikusuiPLZ164W(object):
    """Documentation for a class.

    Represents a Kikusui active load series PLZ.
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

    def set_load_on(self):
        #INPut[:STATe][:IMMediate] {ON|OFF|1|0}
        cmd='INP 1'
        self.port.write_string(cmd)

    def set_load_off(self):
        #INPut[:STATe][:IMMediate] {ON|OFF|1|0}
        cmd='INP 0'
        self.port.write_string(cmd)
        
    def get_operation_mode(self):
        """Specify constant current load mode"""
        #[SOURce:]FUNCtion[:MODE]?
        cmd='FUNC:MODE?'
        self.port.write_string(cmd)

    def set_constant_current_mode(self):
        """Specify constant current load mode"""
        #[SOURce:]FUNCtion[:MODE] {CC|CV|CP|CR|CCCV|CRCV}
        cmd='FUNC:MODE CC'
        self.port.write_string(cmd)

    def set_constant_voltage_mode(self):
        """Specify constant voltage load mode"""
        #[SOURce:]FUNCtion[:MODE] {CC|CV|CP|CR|CCCV|CRCV}
        cmd='FUNC:MODE CV'
        self.port.write_string(cmd)

    def set_constant_power_mode(self):
        """Specify constant power load mode"""
        #[SOURce:]FUNCtion[:MODE] {CC|CV|CP|CR|CCCV|CRCV}
        cmd='FUNC:MODE CP'
        self.port.write_string(cmd)

    def set_constant_resistance_mode(self):
        """Specify constant resistance mode"""
        #[SOURce:]FUNCtion[:MODE] {CC|CV|CP|CR|CCCV|CRCV}
        cmd='FUNC:MODE CR'
        self.port.write_string(cmd)
        
    def set_constant_currentvoltage_mode(self):
        """Specify constant current and voltage mode"""
        #[SOURce:]FUNCtion[:MODE] {CC|CV|CP|CR|CCCV|CRCV}
        cmd='FUNC:MODE CCCV'
        self.port.write_string(cmd)

    def set_constant_resistancevoltage_mode(self):
        """Specify constant resistance and voltage mode"""
        #[SOURce:]FUNCtion[:MODE] {CC|CV|CP|CR|CCCV|CRCV}
        cmd='FUNC:MODE CRCV'
        self.port.write_string(cmd)
        
    def set_current_range_high(self):
        """Set the conductance range. 
        LOWrange=0A-330mA->resolution 0.01mA,
        MEDrange=0A-3.3A->resolution 0.1mA,
        HIGHrange=0A-33A->resolution 1mA, """
        #[SOURce:]CURRent:RANGe {LOW|MEDium|HIGH}
        cmd='CURR:RANG HIGH'
        self.port.write_string(cmd)

    def set_current_range_med(self):
        """Set the conductance range. 
        LOWrange=0A-330mA->resolution 0.01mA,
        MEDrange=0A-3.3A->resolution 0.1mA,
        HIGHrange=0A-33A->resolution 1mA, """
        #[SOURce:]CURRent:RANGe {LOW|MEDium|HIGH}
        cmd='CURR:RANG MED'
        self.port.write_string(cmd)

    def set_current_range_low(self):
        """Set the conductance range. 
        LOWrange=0A-330mA->resolution 0.01mA,
        MEDrange=0A-3.3A->resolution 0.1mA,
        HIGHrange=0A-33A->resolution 1mA, """
        #[SOURce:]CURRent:RANGe {LOW|MEDium|HIGH}
        cmd='CURR:RANG LOW'
        self.port.write_string(cmd)

    def set_current_value(self, value):
        """Specify constant voltage load mode"""
        #[SOURce:]CURRent[:LEVel][:IMMediate][:AMPLitude] {<numeric>|MINimum|MAXimum}
        cmd='CURR '+str(value)
        self.port.write_string(cmd)
        
    def get_measure_current(self):
        """Specify constant voltage load mode"""
        #MEASure[:SCALar]:CURRent[:DC]?
        cmd='MEAS:CURR?'
        value_str = self.port.query(cmd)
        return value_str

    def get_measure_voltage(self):
        """Specify constant voltage load mode"""
        #MEASure[:SCALar]:VOLTage[:DC]?
        cmd='MEAS:VOLT?'
        value_str = self.port.query(cmd)
        return value_str
        
    def get_measure_power(self):
        """Specify constant voltage load mode"""
        #MEASure[:SCALar]:POWer[:DC]?
        cmd='MEAS:POW?'
        value_str = self.port.query(cmd)
        return value_str
                
    def trigger(self, memory_cell):
        """Trigger signal to execute a command"""
        return self.port.write_string("*TRG")


if __name__ == "__main__":

    activeload_port = 0
    activeload_address = 4
    activeload_protocol = 'GPIB'

    gen_port = generic_port.PyVisaPort(activeload_protocol, activeload_address, activeload_port, timeout = DEFAULT_TIMEOUT)
    activeload = KikusuiPLZ164W(gen_port, DEFAULT_TIMEOUT)
    activeload.connect()
    print "  --> gen id: `%s'" % activeload.identify()
    activeload.reset()
    time.sleep(1)
    activeload.set_constant_current_mode()
    activeload.set_current_range_low()
    activeload.set_current_value(.1)
    activeload.set_load_on()
    time.sleep(1)  
    print "  --> out current: `%s'" % activeload.get_measure_current()
    print "  --> out voltage: `%s'" % activeload.get_measure_voltage()
    activeload.set_load_off()    
    activeload.disconnect()

    print "Done"
