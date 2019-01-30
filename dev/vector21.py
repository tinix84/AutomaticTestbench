import sys
sys.path.append('../include/')
import cmdmx_constant
sys.path.append('../utility/')
import lrf_histogram 

import generic_port
import re
import time
import matplotlib.pyplot as plt

DEFAULT_TIME_OUT   = 10
# Sensor Array Data Set Class
class Vector21():
    def __init__(self, port, timeout, sampling_frequency):
        #initialize and configure serial port class
        self.port = port
        self.version = None
        self.info = None
        self.mx_cmd_info = lrf_histogram.MxCommand()
        self.port.set_timeout(timeout)
        self.sampling_frequency = sampling_frequency

    def wakeup(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">\r")
        time.sleep(.5)
        self.port.write_string(">\r")
        self.port.flush()
        self.port.close_stream()

    def getversion(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Iv\r")
        time.sleep(.1)
        version = self.port.read_all()
        self.port.close_stream()
        return version

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
        stream2p = self.port.read_block((cmdmx_constant.WORD_NR_NOISE_DISTR+1)*6)
        histo_size = lrf_histogram.get_hex_param(
          re.findall(r'[A-Z0-9]', stream2p), cmdmx_constant.WORD_NR_HISTO_SIZE)

        apd_distr_len = lrf_histogram.get_hex_param(
          re.findall(r'[A-Z0-9]', stream2p), cmdmx_constant.WORD_NR_NOISE_DISTR)
        print histo_size, apd_distr_len
        stream3p = self.port.read_block(6*(38+apd_distr_len+histo_size)+1)
        self.port.close_stream()
        stream = uc_msg+stream2p+stream3p
        print stream3p
        lrf_histogram.load_data_from_mxstream(self.mx_cmd_info, stream)
#
    def getdistancewithSNR(self):
        if not(self.port.is_open()):
            self.port.open_stream()
        self.port.write_string(">Mc\r")
        stream = self.port.read_all()
        self.port.close_stream()
        return stream


if __name__ == '__main__' :

    sample_frequency = 33e6
    delta_t = 1/sample_frequency
    myport = generic_port.PySerialPort(1,DEFAULT_TIME_OUT,38400)
    myLRF = Vector21(myport, DEFAULT_TIME_OUT, sample_frequency)

    print myLRF.getversion()
    myLRF.getlonghistogram()



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
    plt.plot(myLRF.mx_cmd_info['Histogram']['raw_data'])
    plt.show()
