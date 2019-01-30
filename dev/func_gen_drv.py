# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 07:28:15 2012

@author: tricc
"""
import sys
sys.path.append('../include/')
import time
#import datetime
import generic_port
import debug_msg
#import afg_protocol as afgp


DEFAULT_TIMEOUT = 1

class afgp(object):
    """Represents a Tektronix AFG3102 signal generator protocol."""
    output = { 1: 'OUTPut1', 2: 'OUTPut2', }
    channel = {1: 'SOURce1', 2: 'SOURce2', }

class AFG3102(object):
    """Represents a Tektronix AFG3102 signal generator or similar gen."""

    def __init__(self, port_obj, timeout=DEFAULT_TIMEOUT):
        # Some hard-coded thingies.
        self.port=port_obj

    def is_ethernet(self):
        print debug_msg.TBD_MSG
        #-----

    def is_gpib(self):
        print debug_msg.TBD_MSG

    def is_connected(self):
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
        """Ask the gen for its ID."""
        return self.port.write_string('*RST;*CLS' )

    def query_options(self):
        """Query the gen options."""
        return self.query("*OPT?")

    def set_output_on(self, ch_number):
        #CMD$='OUTPut1:STATe OFF'
        cmd=afgp.output[ch_number]+':STATe ON'
        self.port.write_string(cmd)

    def set_output_off(self, ch_number):
        #CMD$='OUTPut1:STATe OFF'
        cmd=afgp.output[ch_number]+':STATe OFF'
        self.port.write_string(cmd)

    def set_output_impedance(self, ch_number, value='INFinity'):
        #OUTPut1:IMPedance INFinity
        cmd=afgp.output[ch_number]+':IMPedance '+str(value)
        self.port.write_string(cmd)

    def set_voltage_low(self, ch_number, value=0):
        #'SOURce1:VOLTage:LEVel:IMMediate:LOW 0V'
        cmd=afgp.channel[ch_number]+':VOLTage:LEVel:IMMediate:LOW '+str(value)
        self.port.write_string(cmd)

    def set_voltage_high(self, ch_number, value=0):
        #'SOURce1:VOLTage:LEVel:IMMediate:HIGH 3.3V'
        cmd=afgp.channel[ch_number]+':VOLTage:LEVel:IMMediate:HIGH '+str(value)
        self.port.write_string(cmd)

    def set_function_pulse(self, ch_number):
        #SOURce1:FUNCtion:SHAPe PULSe
        cmd=afgp.output[ch_number]+':FUNCtion:SHAPe PULSe'
        self.port.write_string(cmd)

    def set_function_square(self, ch_number):
        pass

    def set_function_ramp(self, ch_number):
        pass

    def set_function_arbitrary(self, ch_number):
        pass

    def set_pulse_period(self, ch_number, value='1us'):
        #SOURce1:PULSe:PERiod 115us
        cmd=afgp.channel[ch_number]+':PULSe:PERiod '+str(value)
        self.port.write_string(cmd)

    def set_pulse_width(self, ch_number, value='1us'):
        #SOURce1:PULSe:WIDTh 84us
        cmd=afgp.channel[ch_number]+':PULSe:WIDTh '+str(value)
        self.port.write_string(cmd)

    def set_pulse_falltime(self, ch_number, value='5ns'):
        #SOURce1:PULSe:TRANsition:TRAiling 5ns
        cmd=afgp.channel[ch_number]+':PULSe:TRANsition:TRAiling '+str(value)
        self.port.write_string(cmd)

    def set_pulse_risetime(self, ch_number, value='5ns'):
        #SOURce1:PULSe:TRANsition:LEADing 5ns
        cmd=afgp.channel[ch_number]+':PULSe:TRANsition:LEADing '+str(value)
        self.port.write_string(cmd)

    def set_pulse_delay(self, ch_number, value='0ms'):
        #SOURce1:PULSe:DELay 0ms
        cmd=afgp.channel[ch_number]+':PULSe:DELay '+str(value)
        self.port.write_string(cmd)

    def set_runmode_burst(self, ch_number):
        #SOURce1:BURSt:STATe ON'
        cmd=afgp.channel[ch_number]+':BURSt:STATe ON'
        self.port.write_string(cmd)

    def set_burst_mode_triggered(self, ch_number):
        #'SOURce1:BURSt:MODE TRIGgered'
        cmd=afgp.channel[ch_number]+':BURSt:MODE TRIGgered'
        self.port.write_string(cmd)

    def set_burst_cycles(self, ch_number, value):
        #'SOURce1:BURSt:NCYCles 7680'
        cmd=afgp.channel[ch_number]+':BURSt:NCYCles '+str(value)
        #print cmd
        self.port.write_string(cmd)

    def set_burst_trigger_delay(self, ch_number, value):
        #'SOURce1:BURSt:TDELay 112us'
        cmd=afgp.channel[ch_number]+':BURSt:TDELay '+str(value)
        self.port.write_string(cmd)

    def save_setup_to_memory(self, mem_number):
        #'*SAV 2'
        cmd='*SAV '+str(mem_number)
        self.port.write_string(cmd)

    def recall_setup_from_memory(self, mem_number):
        #'*RCL 2''
        cmd='*RCL '+str(mem_number)
        self.port.write_string(cmd)

    def trigger(self):
        #'*RCL 2''
        cmd='TRIGger:SEQuence:IMMediate'
        self.port.write_string(cmd)

if __name__ == "__main__":

    gen_address = 4
    gen_port = None
    gen_protocol = 'GPIB'

    gen_port = generic_port.PyVisaPort(gen_protocol, gen_address, gen_port, timeout = DEFAULT_TIMEOUT)
    gen = AFG3102(gen_port, DEFAULT_TIMEOUT)
    gen.connect()
    print "  --> gen id: `%s'" % gen.identify()
    gen.reset()
    time.sleep(1)
    gen.recall_setup_from_memory(3)
    time.sleep(1)
    gen.set_burst_cycles(1, 1)
    gen.set_burst_cycles(2, 1)
    gen.set_burst_trigger_delay(1, 0)
    gen.set_burst_trigger_delay(2, 112e-6)
    gen.set_output_on(1)
    gen.set_output_on(2)
    gen.trigger()
    gen.disconnect()

    print "Done"
