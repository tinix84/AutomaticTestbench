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
import lecroy_protocol as lcp

DEFAULT_TIMEOUT = 1

class LeCroyWaveRunner610Zi(object):
    """Documentation for a class.

    Represents a LeCroy WaveRunner or similar scope.
    """

    def __init__(self, port_obj, timeout = DEFAULT_TIMEOUT):
        """The constructor."""

        self.port = port_obj
        self.acquisition = Acquisition()
        self.cursor = Cursor()
        self.timout = timeout
        #self.Display()
        #self.Hardcopy()
        #self.Math()
        #self.Memory()
        self.saverecall = SaveRecall()

    def meas2num(self, meas_str):
        """Convert measurement string of the scope in number."""
        value = meas_str.split(',')[1]
        try:
            out = float(value)
        except ValueError:
            out = '#'
        return out

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

    def identify(self):
        """Ask the scope for its ID."""
        return self.port.query("*IDN?",1000)

    def query_options(self):
        """Query the scope options."""
        return self.port.query("*OPT?")

    def set_memory_size(self, mem_size):
        """TBD. Set the acquisition memory of the scope."""
        print debug_msg.TBD_MSG

    def get_memory_size(self):
        """TBD. Read the acquisition memory of the scope."""
        print debug_msg.TBD_MSG

    def set_average_sweeps(self, sweeps_number):
        """TBD. Set the number of averaging of the channel ."""
        print debug_msg.TBD_MSG

    def set_bandwidth_limit(self, value='BWFULL'):
        """TBD. Set the bandwitch limit of the channel ."""
        #CMD$=“BWL C1,ON”
        print debug_msg.TBD_MSG

    def get_bandwidth_limit(self):
        """TBD. Set the bandwitch limit of the channel ."""
        print debug_msg.TBD_MSG

    def clear_sweeps(self):
        """TBD. Clear the sweep, restart averaging from 0"""
        print debug_msg.TBD_MSG

    def coupling(self):
        """TBD. Set coupling mode of the channel: DC, AC, 50Ohm"""
        print debug_msg.TBD_MSG

    def find_scale(self):
        """TBD. Ask channel vertical scale"""
        print debug_msg.TBD_MSG

    def invert(self, state = False):
        """TBD. Ask invert channel polarity"""
        print debug_msg.TBD_MSG

    def probe_attenuation(self):
        """TBD. Set probe attenuation"""
        print debug_msg.TBD_MSG

    def set_vert_offset(self, value = 0):
        """TBD. Set vertical offset"""
        #CMD$=“C2:OFST -3V”:
        print debug_msg.TBD_MSG

    def get_vert_offset(self, osc_obj, read_buffer_size = 1000):
        """TBD. Get vertical offset"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        pass

    def set_vert_scale(self):
        """TBD."""
        print debug_msg.TBD_MSG

    def set_hor_offset(self):
        """TBD."""
        print debug_msg.TBD_MSG

    def set_hor_scale(self):
        """TBD."""
        print debug_msg.TBD_MSG

    def get_meas_amplitude(self, source):
        """Get signal amplitude"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? AMPL'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_area(self, source):
        """Get signal integral"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? area'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_cyclesnumber(self, source):
        """Get the number of signal cycle"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? CYCL'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_falltime90to10(self, source):
        """Get fall time from 90% to 10% """
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? FALL'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_frequency(self, source):
        """Get signal frequency"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? FREQ'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_max(self, source):
        """Get signal maximimum"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? MAX'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_mean(self, source):
        """Get signal mean"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? MEAN'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_min(self, source):
        """Get signal minimum"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? MIN'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_peak2peak(self, source):
        """Get signal peak to peak value"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? PKPK'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_period(self, source):
        """Get signal period"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? PER'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_risetime10to90(self, source):
        """Get rise time from 10% to 90% """
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? RISE'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_rootmeansquare(self, source):
        """Get signal RMS value"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? RMS'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_standarddeviation(self, source):
        """Get signal stansard deviation"""
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? SDEV'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_top(self, source):
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? TOP'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_width(self, source):
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? WID'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def get_meas_width_neg(self, source):
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        cmd =source+':PAVA? widthn'
        value_str = self.port.query(cmd)
        return self.meas2num(value_str)

    def print_screen_tif(self, filename):
        # QUERY SYNTAX  <channel> :  OFfSeT ?
        # RESPONSE FORMAT  <channel> :  OFfSeT  <offset>
        self.port.tty.StoreHardcopyToFile('TIFF', '', filename)


    def Maximize(self):
        pass

    def MaxSamples(self):
        pass

    def NumSegments (self):
        pass

    def SampleMode(self):
        pass

    def SamplingRate(self):
        pass

    def get_timespan(self):
        """Return the timespan of the horizontal axis."""
        # NOTE: Scopes seem to always have a grid of 10x10 divisions,
        # so we just multiply the time/div by 10.
        time_per_div = float(self.port.query("TIME_DIV?"))
        timespan = 10. * time_per_div

        # End of get_timespan().
        return timespan

    def set_timespan(self, timespan):
        """Adjust the timebase such that at least timespan fits in."""

        # NOTE: Scopes seem to always have a grid of 10x10 divisions,
        # so we just divide the timespan by t10 to obtain the
        # time/div.

        time_per_div = .1 * timespan
        self.port.write_string("TIME_DIV %.12fS" % time_per_div)

    def recall_setup_from_file(self, filename = None):
        cmd="RCPN DISK, HDD, FILE,"+filename
        self.port.write_string(cmd)

class Acquisition(object):
#ACQUISITION — TO CONTROL WAVEFORM CAPTURE
#ARM ARM_ACQUISITION Changes acquisition state from “stopped” to “single.”
#ASET AUTO_SETUP Adjusts vertical, timebase and trigger parameters for signal display.
#ATTN ATTENUATION Selects the vertical attenuation factor of the probe.
#BWL BANDWIDTH_LIMIT Enables or disables the bandwidth-limiting low-pass filter.
#CPL COUPLING Selects the specified input channel’s coupling mode.
#OFST OFFSET Allows vertical offset adjustment of the specified input channel.
#MSIZ MEMORY_SIZE Allows selection of maximum memory length.
#SEQ SEQUENCE Controls the sequence mode of acquisition.
#STOP STOP Immediately stops signal acquisition.
#VDIV VOLT_DIV Sets the vertical sensitivity in volts/div.
#WAIT WAIT Prevents new command analysis until current acquisition completion.

    def __init__(self):
        self.aux_input = None #TBD
        self.aux_output = None #TBD
        self.c1 = ChannelOsc(1)
        self.c2 = ChannelOsc(2)
        self.c3 = ChannelOsc(3)
        self.c4 = ChannelOsc(4)
        self.horizontal = HorizontalOsc()
        self.trigger = TriggerOsc()


class ChannelOsc(object):
    def __init__(self, ch_number):
        self.name = lcp.channel[ch_number]

class HorizontalOsc(object):
#TDIV TIME_DIV Modifies the timebase setting.

    def __init__(self):
        pass


class TriggerOsc(object):
#FRTR FORCE_TRIGGER Forces the instrument to make one acquisition.
#*TRG *TRG Executes an ARM command.
#TRCP TRIG_COUPLING Sets the coupling mode of the specified trigger source.
#TRDL TRIG_DELAY Sets the time at which the trigger is to occur.
#TRLV TRIG_LEVEL Adjusts the level of the specified trigger source.
#TRMD TRIG_MODE Specifies Trigger mode.
#TRPA TRIG_PATTERN Defines a trigger pattern.
#TRSE TRIG_SELECT Selects the condition that will trigger acquisition.
#TRSL TRIG_SLOPE Sets the slope of the specified trigger source.

    def __init__(self):
        pass


class Cursor(object):
#CRMS CURSOR_MEASURE Specifies the type of cursor or parameter measurement for display.
#CRST CURSOR_SET Allows positioning of any cursor.
#CRVA? CURSOR_VALUE? Returns the values measured by the specified cursors for a given trace.
#CRS CURSORS Sets the cursor type.
#OFCT OFFSET_CONSTANT Sets offset to be constant in divisions or volts.
#PARM PARAMETER Controls the parameter mode.
#PACL PARAMETER_CLR Clears all current parameters in Custom and Pass/Fail modes.
#PACU PARAMETER_CUSTOM Controls parameters with customizable qualifiers.
#PADL PARAMETER_DELETE Deletes a specified parameter in Custom and Pass/Fail modes.
#PAST? PARAMETER_STATISTICS Returns parameter statistics results.
#PAVA? PARAMETER_VALUE? Returns current value(s) of parameter(s) and mask tests.
#PF PASS_FAIL Sets up the Pass / Fail system.
#PFDO PASS_FAIL_DO Defines outcome and actions for the Pass/Fail system.
#PECS PER_CURSOR_SET Positions one of the six independent cursors.
    pass

class Function(object):
#FUNCTION — TO PERFORM WAVEFORM MATHEMATICAL OPERATIONS
#CLM CLEAR_MEMORY Clears the specified memory.
#CLSW CLEAR_SWEEPS Restarts the cumulative processing functions.
#DEF DEFINE Specifies math expression for function evaluation.
#FCR FIND_CENTER_RANGE Automatically sets the center and width of a histogram.
#FRST FUNCTION_RESET Resets a waveform processing function.
#HARD COPY — TO PRINT THE CONTENTS OF THE DISPLAY
#HCSU HARDCOPY_SETUP Configures the hard-copy driver.
#SCDP SCREEN_DUMP Initiates a screen dump.
    pass

class Miscellaneous(object):
#ACAL AUTO_CALIBRATE Enables or disables automatic calibration
#BUZZ BUZZER Controls the buzzer in the instrument.
#*CAL? *CAL? Performs a complete internal calibration
#DIR DIRECTORY Creates or deletes directories, or changes the current directory.
#*IDN? *IDN? Used for identification purposes.
#*OPT? *OPT? Identifies the installed oscilloscope options.
#*TST? *TST? Performs internal self-test.
    pass

class SaveRecall(object):
#SAVE/RECALL SETUP — TO PRESERVE AND RESTORE FRONT PANEL SETTINGS
#*RCL *RCL Recalls one of five non-volatile panel setups.
#RCPN RECALL_PANEL Recalls a front panel setup from mass storage.
#*RST *RST Initiates a device reset.
#*SAV *SAV Stores the current state in non-volatile internal memory.
#STPN STORE_PANEL Stores the complete front panel setup on a mass-storage file.
    pass



######################################################################
## Main entry point.
######################################################################

if __name__ == "__main__":

    scope_address = '192.168.1.10'
    scope_lan_port = 1861
    scope_protocol = 'TCPIP'

    scope_port = generic_port.ActiveXLeCroyPort(scope_protocol, scope_address, None, DEFAULT_TIMEOUT)
    scope = LeCroyWaveRunner610Zi(scope_port, DEFAULT_TIMEOUT)
    scope.connect()
    print "  --> scope id: `%s'" % scope.identify()
    scope.recall_setup_from_file('D:\GaNTxPWM150us')
    time.sleep(1)
    f1 = lcp.function[1]
    print f1
    print scope.get_meas_area(f1)
    scope.print_screen_tif('test.tif')
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
