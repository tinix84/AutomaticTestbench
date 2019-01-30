import sys
sys.path.append('../include/')
import cmdmx_constant
sys.path.append('../lib/')
import lrf_histogram, savemx, savemxjson

import generic_port
import re
import time
import matplotlib.pyplot as plt

DEFAULT_TIME_OUT   = 30
# Sensor Array Data Set Class
class MBModC():
    def __init__(self, port, timeout, sampling_frequency):
        #initialize and configure serial port class
        self.port = port
        self.version = None
        self.info = None
        self.EEPROMparameter=None
        self.mc_cmd_info=None
        self.mx_cmd_info = lrf_histogram.MxCommand()
        self.port.set_timeout(timeout)
        self.sampling_frequency = sampling_frequency
        self.EPCSType = None        
        self.FPGAType = None
        self.uCType = None        
        self.EPCSreadfile = None
        self.EPCSprogfid = None
        self.EPCSprogsize = None
        self.EPCSprogdata = None
        self.EPCSDensity = None


    def wakeup(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Is\r")
        time.sleep(.1)

    def wakeupDSP(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Xp\r")
        time.sleep(.1)
        
    #Checks whether the Nucleus/ModC firmware is responding to the PC over
    #specified serial port.
    #Returns true if the firmware responded and false otherwise.
    def isFirmwareResponding(self):
      RESPONSE_LENGTH_TRESHOLD = 20;
      #Let's wake the micro controller up
      self.wakeup()
    
      #Let's ask for informations.
      output = self.port.getversion()
      if (len(output) >= RESPONSE_LENGTH_TRESHOLD):
          if (output.rfind("/") >= 0):
              return True
      else:
          return False

    def getversion(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Iv\r")
        time.sleep(.1)
        version = self.port.read_all()
        self.port.close_stream()
        return version

    def getEEPROMparameter(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Zh\r")
        time.sleep(1)
        EEPROMparameter = self.port.read_all()
        self.port.close_stream()
        return EEPROMparameter
       
    def getinfo(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Is\r")
        time.sleep(.1)
        info = self.port.read_all()
        self.port.close_stream()
        return info

    def getshorthistogram(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">My\r")
        time.sleep(.1)
        stream = self.port.read_all()
        self.port.close_stream()
        return stream

    def getlonghistogram(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Mx\r")
        time.sleep(.1)

        c = None
        uc_msg = []
        while (c != '*'):
            c = self.port.read_block(1)
            uc_msg.append(c)

        uc_msg=''.join(uc_msg)
        print uc_msg
        stream2p = self.port.read_block((cmdmx_constant.WORD_NR_NOISE_DISTR+1)*6)
        print stream2p
        histo_size = lrf_histogram.get_hex_param(
          re.findall(r'[A-Z0-9]', stream2p), cmdmx_constant.WORD_NR_HISTO_SIZE)

        apd_distr_len = lrf_histogram.get_hex_param(
          re.findall(r'[A-Z0-9]', stream2p), cmdmx_constant.WORD_NR_NOISE_DISTR)
        print histo_size, apd_distr_len
        #+3 is due to characters \n< at the end of msg
        stream3plen=(6*(103-cmdmx_constant.WORD_NR_NOISE_DISTR-1+apd_distr_len+histo_size))+3
        stream3p = self.port.read_block(stream3plen)
        self.port.close_stream()
        stream = uc_msg+stream2p+stream3p
        print stream3p
        lrf_histogram.load_data_from_mxstream(self.mx_cmd_info, stream)
        return stream
#
    def getdistancewithSNR(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Mc\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream
        
    def getmeasurement3targets(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Md1\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream

    def getmeasurement5targets(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Md5\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream

    def setLPCLModeOFF(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Tl1,0\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream
    
    def setLPCLMode100Hz(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Tl1,1\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream
    
    def setLPCLMode200Hz(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Tl1,2\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream
        
    def setLPCLMode400Hz(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Tl1,3\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream
        
    def setLPCLMode800Hz(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Tl1,4\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream

    def setLPCLMode1600Hz(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Tl1,5\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream
        
    def setLPCLMode3200Hz(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Tl1,6\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream
        
        
if __name__ == '__main__' :

    measureNr=1
    sample_frequency = 100e6
    delta_t = 1/sample_frequency
    myport = generic_port.PySerialPort(1,DEFAULT_TIME_OUT,57600)
    myLRF = MBModC(myport, DEFAULT_TIME_OUT, sample_frequency)

    directory='../HistoryLogs/'
    user='TRICC'
    comment='TestHBWRX100k10pF680_HIGHGAIN'
    
    myLRF.version = myLRF.getversion()
    time.sleep(.1)
    myLRF.EEPROMparameter = myLRF.getEEPROMparameter()
    myLRF.mc_cmd_info = getdistancewithSNR()
    
    for iter in range(1,measureNr+1):
        fapd = plt.figure(1)
        fhisto = plt.figure(2)
        
        myLRF.getlonghistogram()
        time.sleep(1)
        plt.plot(myLRF.mx_cmd_info['Histogram']['raw_data'])
        plt.figure(1)
        plt.plot(myLRF.mx_cmd_info['Apd']['noise_distribution'])
        plt.figure(2)
        savemx.save(myLRF, directory, user, comment)
        

#  #initialise and open port
#  read_filename = './Mx120508193220.txt'
#  file = open(read_filename, 'r')
##  print file.read()
#  char = None
#  while (char <> '*'):
#      char = file.read(1)          # read by character
#      if not char: break
#      print char,
#
#  stream2p = file.read(65*6)
#  print stream2p
#  stream2p = re.findall(r'[A-Z0-9]', stream2p)
#  histo_size = lrf_histogram.get_hex_param(stream2p, 
#                                        cmdmx_constant.WORD_NR_HISTO_SIZE)
#  apd_distr_len = lrf_histogram.get_hex_param(stream2p, 
#                                        cmdmx_constant.WORD_NR_NOISE_DISTR)
#  print histo_size
#  print apd_distr_len
#  file.close()


    #myLRF.mx_cmd_info.load_data_from_mxstream(stream)
    plt.show()
    
