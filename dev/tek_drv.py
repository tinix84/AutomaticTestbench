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
# how long to sleep after issuing a write
DEFAULT_SLEEPTIME = 0.01

class TektronikTDS420A(object):
    """
    TDS Family Digitizing Oscilloscopes (TDS 410A, 420A, 460A, 
    520A, 524A, 540A, 544A,
    620A, 640A, 644A, 684A, 744A & 784A)
    """
    
#    def Channel(self, number):
#    """The dictionary to describe channel oscilloscope"""
#        ch={}
#        ch['number'] = number
#        ch['scale'] = 0
#        ch['position'] = 0
#        ch['offset'] = 0
#        ch['coupling'] = 0
#        ch['impedance'] = 0
#        ch['bandwidth'] = 0
#        return ch

    def __init__(self, port_obj, timeout = DEFAULT_TIMEOUT):
        """The constructor."""
        self.port = port_obj
#        self['CH1'] = self.channel(1)
#        self['CH2'] = self.channel(1)
#        self['CH3'] = self.channel(1)
#        self['CH4'] = self.channel(1)
        self.timeout = timeout
        #self.Display()
        #self.Hardcopy()
        #self.Math()
        #self.Memory()
        
    def beep(self):
        self.port.write_string('BELl')
        
    def clear_status(self):
        self.port.write_string('*CLS')
    
    def is_busy(self):
        """Returns the status of the digitizing oscilloscope"""
        return self.port.query("BUSY?",1000)

    def is_ethernet(self):
        """TBD. Check if the connection is ethernet."""
        print debug_msg.TBD_MSG

    def is_gpib(self):
        """TBD. Check if the connection is GPIB."""
        print debug_msg.TBD_MSG

    def is_connected(self):
        """TBD. Check if the connection is established."""
        print debug_msg.TBD_MSG

    def connect(self):
        """Connect to the scope."""
        self.port.open_stream()

    def disconnect(self):
        """Disconnect if connected."""
        self.port.close_stream()

    def info(self):
        """Returns identifying information about the instrument and its firmware."""
        return self.port.query("ID?",1000)
    
    def identify(self):
        """Returns the digitizing oscilloscope identification code."""
        return self.port.query("*IDN?",1000)

    def query_options(self):
        """Query the scope options. TDS 5XXA, 6XXA, & 7XXA Only"""
        return self.port.query("*OPT?")

    def set_memory_size(self, ref_no = 1, mem_size = 500):
        """Sets or queries the number of waveform data points 
        for the specified reference"""
        cmd='ALLOcate:WAVEform:REF%d %d'% (ref_no, mem_size)
        self.port.write_string(cmd)

    def get_memory_size(self):
        """Returns the number of data points allocated for 
        all four reference memory locations."""
        return self.port.query("ALLOcate:WAVEform?")

    def set_average_sweeps(self, sweeps_number):
        """TBD. Set the number of averaging of the channel ."""
        print debug_msg.TBD_MSG

    def set_bandwidth_limit(self, ch_no=1, value='FULL'):
        """Sets or queries the bandwidth setting of the specified channel. This is equivalent
        to setting Bandwidth in the Vertical menu."""
        if value == 'LOW':
            bw_str = 'TWEnty'
        if value == 'HIGH':
            bw_str = 'HUNdred' #valid for all TDS except 648A&7XXA where is TWOfifty
        if value == 'FULL':
            bw_str = 'FULl' #valid for all TDS except 648A&7XXA where is TWOfifty
        cmd='CH%d:BANdwidth %s'% (ch_no, bw_str)
        self.port.write_string(cmd)

    def get_bandwidth_limit(self, ch_no=1):
        """Get the bandwitch limit from the channel obj."""
        cmd='CH%d:BANdwidth?'% (ch_no)
        return self.port.query(cmd)
        
    def set_channel_coupling(self, ch_no=1, value='DC'):
        """Sets or queries the input attenuator coupling setting of the specified channel.
        CH<x>:COUPling {AC¦DC¦GND}"""
        cmd='CH%d:COUPling %s'% (ch_no, value)
        self.port.write_string(cmd)

    def get_channel_coupling(self, ch_no=1):
        """Sets or queries the input attenuator coupling setting of the specified channel.
        CH<x>:COUPling {AC¦DC¦GND}"""
        cmd='CH%d:COUPling?'% (ch_no)
        return self.port.query(cmd)

    def set_channel_impedance(self, ch_no=1, value='MEG'):
        """Sets the input attenuator coupling setting of the specified channel.
        CH<x>:IMPedance {FIFty¦MEG}"""
        cmd='CH%d:IMPedance %s'% (ch_no, value)
        self.port.write_string(cmd)

    def get_channel_impedance(self, ch_no=1):
        """Queries the input attenuator coupling setting of the specified channel.
        CH<x>:IMPedance {FIFty¦MEG}"""
        cmd='CH%d:IMPedance?'% (ch_no)
        return self.port.query(cmd)        
        
    def get_channel_parameter(self, ch_no=1):
        """TBD. parsing of obj."""
        cmd='CH%d?'% (ch_no)
        return self.port.query(cmd)

    def set_offset(self, ch_no=1, value = 0):
        """Sets the offset in volts"""
        #CMD$=“CH<x>:OFFSet <NR3>”:
        cmd='CH%d:OFFSet %d'% (ch_no, value)
        self.port.write_string(cmd)

    def get_offset(self, ch_no=1):
        """Queries the offset in volts"""
        cmd='CH%d:IMPedance?'% (ch_no)
        return self.port.query(cmd)    

    def get_attenuation(self, ch_no=1):
        """Returns the attenuation factor of the probe that is 
        attached to the specified channel."""
        cmd='CH%d:PRObe?'% (ch_no)
        return self.port.query(cmd)    
        
    def set_scale(self, ch_no=1, value = 0):
        """Sets the vertical gain in volts of the specified channel"""
        #CMD$=“CH<x>:SCALe <NR3>”:
        cmd='CH%d:SCALe %d'% (ch_no, value)
        self.port.write_string(cmd)

    def get_scale(self, ch_no=1):
        """Queries the vertical gain of the specified channel"""
        cmd='CH%d:SCALe'% (ch_no)
        return self.port.query(cmd)    

    def get_meas_amplitude(self, ch_no):
        """Get signal amplitude"""
        self.port.write_string('MEASUrement:IMMed:TYPe AMPlitude')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')
        
    def get_meas_rms(self, ch_no):
        """Get signal amplitude"""
        self.port.write_string('MEASUrement:IMMed:TYPe RMS')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')    

    def get_meas_area(self, ch_no):
        """Get signal integral"""
        self.port.write_string('MEASUrement:IMMed:TYPe AREa')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_falltime90to10(self, ch_no):
        """Get fall time from 90% to 10% """
        self.port.write_string('MEASUrement:IMMed:TYPe FALL')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_frequency(self, ch_no):
        """Get signal frequency"""
        self.port.write_string('MEASUrement:IMMed:TYPe FREQ')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_max(self, ch_no):
        """Get signal maximimum"""
        self.port.write_string('MEASUrement:IMMed:TYPe MAX')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_mean(self, ch_no):
        """Get signal mean"""
        self.port.write_string('MEASUrement:IMMed:TYPe MEAN')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_min(self, ch_no):
        """Get signal minimum"""
        self.port.write_string('MEASUrement:IMMed:TYPe MINI')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_peak2peak(self, ch_no):
        """Get signal peak to peak value"""
        self.port.write_string('MEASUrement:IMMed:TYPe PK2pk')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_period(self, ch_no):
        """Get signal period"""
        self.port.write_string('MEASUrement:IMMed:TYPe PERI')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_risetime10to90(self, ch_no):
        """Get rise time from 10% to 90% """
        self.port.write_string('MEASUrement:IMMed:TYPe RISe')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_width(self, ch_no):
        """distance (time) between MidRef (usually 50%) amplitude points of
        a positive pulse """
        self.port.write_string('MEASUrement:IMMed:TYPe PWIdth')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_meas_width_neg(self, ch_no):
        """is the distance (time) between MidRef (usually 50%) amplitude points of
        a negative pulse."""
        self.port.write_string('MEASUrement:IMMed:TYPe NWIdth')
        cmd='MEASUrement:IMMed:SOURCE CH%d'% (ch_no)
        self.port.write_string(cmd)
        time.sleep(DEFAULT_SLEEPTIME)
        return self.port.query('MEASUrement:IMMed:VALue?')

    def get_horizontal_scale(self):
        """Returns the time per division of the main time base."""
        time_per_div = float(self.port.query("HORizontal:MAIn:SCAle?"))
        # End of get_timespan().
        return time_per_div

    def set_horizontal_scale(self, time_per_div):
        """Sets the time per division for the main time base."""
        cmd = "HORizontal:MAIn:SCAle %.2f" % time_per_div
        self.port.write_string(cmd)

    def recall_setup_from_file(self, filename = None):
        cmd="RECAll:SETUp "+ filename
        self.port.write_string(cmd)
        
    def recall_setup_factory(self):
        cmd="RECAll:SETUp FACtory"
        self.port.write_string(cmd)
    
    def recall_setup_memory(self, mem_cell = 1):
        cmd="RECAll:SETUp %d" % mem_cell
        self.port.write_string(cmd)
        
    def get_screen_bmp(self, filename=None, show=False):
        self.port.set_timeout(10)
        self.port.write_string("HEADer ON")
        self.port.write_string("VERBose ON")
        cmd="HARDCOPY:PORT %s" % self.port.protocol
        self.port.write_string(cmd)
        self.port.write_string("HARDCopy:FORMat BMP")
#        self.port.write_string("HARDCOPY START")
#        time.sleep(1)
#        data = self.port.read_string()
        try:
            self.port.write_string("HARDCopy STARt")
            data = self.port.read_string()
            fid = open(filename, 'wb')
            fid.write(data)
            fid.close()
###            self.port.query('*opc?')
        except:
            print "PROBLEM"
        self.port.set_timeout(1)

        return filename
        



######################################################################
## Main entry point.
######################################################################

if __name__ == "__main__":

    scope_protocol = 'GPIB'
    scope_board = 0
    scope_address = 1

    scope_port = generic_port.PyVisaPort(scope_protocol, scope_address, scope_board, DEFAULT_TIMEOUT)
    scope = TektronikTDS420A(scope_port, DEFAULT_TIMEOUT)
    scope.connect()
    print "  --> scope id: `%s'" % scope.identify()

    time.sleep(1)

    scope.get_screen_bmp('test.bmp')
#    DSO.WriteString('f1:PAVA? top', 1)
#    print DSO.ReadString(1000)
#    DSO.WriteString('f1:PAVA? width', 1)
#    print DSO.ReadString(1000)
#    DSO.WriteString('f1:PAVA? area', 1)
#    print DSO.ReadString(1000)
#    DSO.WriteString('c1:PAVA? max', 1)
#    print DSO.ReadString(1000)
#    DSO.WriteString('c2:PAVA? max', 1)
#    print DSO.ReadString(1000)
#    DSO.WriteString('c2:PAVA? area', 1)
#    print DSO.ReadString(1000)
#    DSO.StoreHardcopyToFile('TIF', '', 'imagename.tif');
    scope.disconnect()

    print "Done"
