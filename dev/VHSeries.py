import sys
sys.path.append('../include/')
sys.path.append('../lib/')

import generic_port
import timestamp
import datetime
import re
import time

DEFAULT_TIMEOUT   = 30
# Sensor Array Data Set Class
class VHSeries():
    def __init__(self, port, timeout):
        #initialize and configure serial port class
        self.port = port
        self.protocolVersion = None
        self.identManufacturer = None
        self.identModel=None
        self.identSerialNumber=None

    def getProtocolVersion(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("?\r")
        time.sleep(.1)
        version = self.port.read_all()
        self.port.close_stream()
        return version

    def getIdentManufacturer(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vDm?\r")
        time.sleep(.1)
        manufacturer = self.port.read_all()
        self.port.close_stream()
        return str(manufacturer)
        
    def getIdentModel(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vDM?\r")
        time.sleep(.1)
        model = re.findall(r'vDM(.*?)\r\n', self.port.read_all())      
        self.port.close_stream()
        return str(model)
       
    def getIdentSerialNumber(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vDS?\r")
        time.sleep(.1)
        serialno = re.findall(r'vDS(.*?)\r\n', self.port.read_all())   
        self.port.close_stream()
        return str(serialno)

    def getIdentSoftwareVersion(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vDV?\r")
        time.sleep(.1)
        swversion = re.findall(r'vDV(.*?)\r\n', self.port.read_all())   
        self.port.close_stream()
        return str(swversion)

    def getIdentUPSComProtVersion(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vDC?\r")
        time.sleep(.1)
        protversion = re.findall(r'vDC(.*?)\r\n', self.port.read_all())   
        self.port.close_stream()
        return str(protversion)

    def getControlShutdownAfterDelay(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vCb?\r")
        time.sleep(.1)
        shutdown_timer = self.port.read_all()
        self.port.close_stream()
        return int(shutdown_timer)

    def setControlShutdownAfterDelay(self, delay):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vCb?\r")
        time.sleep(.1)

    def getUpsAlarmGroupA(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vAa?\r")
        time.sleep(.1)
        alarm = self.port.read_all()
        self.port.close_stream()
        #round brackets (\d+) are important to recall number after
        pattern=re.compile(r'vAa(\d+)')
        match=pattern.search(alarm)
        return int(match.group(1))
        
    def getUpsInputLineBads(stream):
    	 pass
    def getUpsBypassVoltage(stream):
    	 pass
    def getUpsBypassFrequency(stream):
    	 pass
    def getUpsBypassCurrent(stream):
    	 pass
    def getUpsBypassPower(stream):
    	 pass
    def getUpsOutputVoltage(stream):
    	 pass
    def getUpsOutputFrequency(stream):
    	 pass
    def getUpsOutputCurrent(stream):
    	 pass
    def getUpsOutputPower(stream):
    	 pass
    def getUpsOutputVA(stream):
    	 pass
    def getUpsOutputPercentLoad(stream):
    	 pass
    def getUpsOutputSource(stream):
    	 pass

    def getUpsBatteryVoltage(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vBU?\r")
        time.sleep(.1)
        stream = self.port.read_all()
        self.port.close_stream()
        pattern=re.compile(r'vBU(\d+)')
        match=pattern.search(stream)
        return float(match.group(1))/10.0
    
#    def getUpsBatteryVoltage(stream):
#        #round brackets (\d+) are important to recall number after
#        pattern=re.compile(r'vBU(\d+)')
#        match=pattern.search(stream)
#        return float(match.group(1))/10.0
        
    def getUpsBatteryCurrent(self):
        #round brackets (\d+) are important to recall number after
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vBI?\r")
        time.sleep(.1)
        stream = self.port.read_all()
        self.port.close_stream()
        pattern=re.compile(r'vBI(\d+)')
        match=pattern.search(stream)
        return int(match.group(1))
        
    def getUpsBatteryTemperature(self):
        #round brackets (\d+) are important to recall number after
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vBT?\r")
        time.sleep(.1)
        stream = self.port.read_all()
        self.port.close_stream()
        pattern=re.compile(r'vBT(\d+)')
        match=pattern.search(stream)
        return int(match.group(1))
        
    def getUpsBatteryEstimatedMinutesRemaining(self):
        #round brackets (\d+) are important to recall number after
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vBt?\r")
        time.sleep(.1)
        stream = self.port.read_all()
        self.port.close_stream()
        pattern=re.compile(r'vBt(\d+)')
        match=pattern.search(stream)
        return int(match.group(1))
        
    def getUpsBatteryEstimatedChargeRemaining(self):
        #round brackets (\d+) are important to recall number after
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vBC?\r")
        time.sleep(.1)
        stream = self.port.read_all()
        self.port.close_stream()
        pattern=re.compile(r'vBC(\d+)')
        match=pattern.search(stream)
        return int(match.group(1))
    
    def getUpsBatteryStatus(self):
        #round brackets (\d+) are important to recall number after
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vBS?\r")
        time.sleep(.1)
        stream = self.port.read_all()
        self.port.close_stream()
        pattern=re.compile(r'vBS(\d+)')
        match=pattern.search(stream)
        return int(match.group(1))
    
    def getUpsInputVoltage(self):
        #round brackets (\d+) are important to recall number after
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string("vI0U?\r")
        time.sleep(.1)
        stream = self.port.read_all()
        self.port.close_stream()
        pattern=re.compile(r'vI0U(\d+)')
        match=pattern.search(stream)
        return int(match.group(1))

        
    def getUpsInputFrequency(stream):
    	 pass
    def getUpsInputCurrent(stream):
    	 pass
    def getUpsInputTruePower(stream):
    	 pass
    def getUpsInputVoltageMin(stream):
    	 pass
    def getUpsInputVoltageMax(stream):
    	 pass       

def init_report(self):
    self.log_directory = './HistoryLogs/'
    time_filename = timestamp('_')
    self.meas_filename = self.log_directory+time_filename+'upsmeas.txt'

    meas_header = []
    meas_header.append('UPS meas starts @:'+str(datetime.datetime.now()))
    meas_header.append("Measure#")
    meas_header.append("BatteryVoltage")
    meas_header.append("BatteryEstimatedMinutesRemaining")
    meas_header.append("getUpsAlarmGroupA")
    meas_header.append("getUpsBatteryStatus")

    self.meas_file = open(self.meas_filename,'a')
    self.meas_file.write(meas_header)

    self.meas_file.close()

class UPSBattVoltageTset():
    def __init__(self):
        #Initialization
        self.meas_list = []
        
        self.log_directory = None
        self.meas_filename = None
        self.log_filename = None
        self.meas_file = None
        self.log_file = None
        self.prtsc_filename = None
        
if __name__ == '__main__' :


    measureNr = 10
    
    myport = generic_port.PySerialPort(protocol = "SERIAL", port = 5, timeout = DEFAULT_TIMEOUT, baud = 1200)
    myUPS = VHSeries(myport, DEFAULT_TIMEOUT)
    
    myUPS.identModel = myUPS.getIdentModel()
    print myUPS.identModel

    for iter in range(1,measureNr+1): 
        meas= []
        meas.append(iter)
        meas.append(myUPS.getUpsBatteryVoltage())
        meas.append(myUPS.getUpsAlarmGroupA())
        meas.append(myUPS.getUpsBatteryVoltage())
        meas.append(myUPS.getUpsBatteryEstimatedMinutesRemaining())
        meas.append(myUPS.getUpsBatteryStatus())

        print meas

        