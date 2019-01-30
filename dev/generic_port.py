"""@package docstring
Documentation for this module.

More details.
"""

import sys
import time
import serial as ser
import win32com.client

sys.path.append('./utility/')
sys.path.append('../include/')
import debug_msg

#requires VISA library
try:
    from  pyvisa.vpp43 import visa_library
    visa_library.load_library(r"C:\WINDOWS\system32\agvisa32.dll")
except WindowsError:
    print "Agilent VISA not found"
try:
    import visa
except:
    print "VISA module not working"

if sys.version_info >= (3, 0):
    def data(string):
        return bytes(string, 'latin1')
    bytes0to255 = bytes(range(256))
else:
    def data(string):
        return string
    bytes0to255  =  ''.join([chr(x) for x in range(256)])

def segments(datain, size = 16):
    for index in range(0, len(datain), size):
        yield datain[index:index+size]

DEFAULT_PORT  =  "1"
DEFAULT_BAUD_RATE = 57600
DEFAULT_TIMEOUT = 100
DEFAULT_BUFFER_SIZE = 1000
DEFAULT_WAIT_TIME = .1
DEFAULT_FILE = None

class PySerialPort():
    """Documentation for a class.

    More details.
    """
    def __init__(self, protocol = "SERIAL", port = DEFAULT_PORT, timeout = DEFAULT_TIMEOUT, 
                     baud = DEFAULT_BAUD_RATE):
        """The constructor:initialize and configure serial port class"""
        self.protocol = "SERIAL"
        self.tty = ser.Serial()
        self.set_serial_port("COM"+ str(port))
        self.set_baud_rate(baud)
        self.set_timeout(timeout)

    def is_open(self):
        """Documentation for a method."""
        return self.tty.isOpen()

    def get_port(self):
        """Documentation for a method."""
        return self.tty.port

    def get_baud_rate(self):
        """Documentation for a method."""
        return self.tty.baudrate

    def get_timeout(self):
        """Documentation for a method."""
        return self.tty.timeout

    def set_serial_port(self, port):
        """Documentation for a method."""
        self.tty.port = port

    def set_baud_rate(self, baud):
        """Documentation for a method."""
        self.tty.baudrate = baud

    def set_timeout(self, timeout):
        """Documentation for a method."""
        self.tty.timeout = timeout

    def open_stream(self):
        """Documentation for a method."""
        self.tty.open()

    def close_stream(self):
        """Documentation for a method."""
        self.tty.close()

    def write_block(self, stream, blocksize):
        """Documentation for a method."""
        for block in segments(stream, blocksize):
            self.tty.write(block)
            #time.sleep(DEFAULT_WAIT_TIME)

    def read_block(self, blocksize):
        """Documentation for a method."""
        stream = self.tty.read(blocksize)
        return stream

    def word_received(self):
        """Documentation for a method."""
        word_received = (self.tty.inWaiting())
        #stream = self.tty.readall()
        return word_received

    def read_all(self):
        """Documentation for a method."""
        stream = self.tty.read(self.tty.inWaiting())
        #stream = self.tty.readall()
        return stream

    def set_timeout_ms(self, timeout):
        """Documentation for a method."""
        self.tty.timeout = timeout

    def read_string(self):
        """Documentation for a method."""
        stream = self.tty.readline()
        return stream

    def write_string(self, stream, wait_time = DEFAULT_WAIT_TIME):
        """Documentation for a method."""
        self.tty.write(stream)
        time.sleep(wait_time)

    def query(self, cmd, read_buffer_size):
        """Documentation for a method."""
        self.write_string(cmd)
        return self.tty.read(read_buffer_size)

    def flush(self):
        """Documentation for a method."""
        self.tty.flushInput()
        self.tty.flushOutput()

    def free(self):
        """Documentation for a method."""
        self.tty.__del__()
       
#class DummyFilePort():
#    """Documentation for a class.
#
#    More details.
#    """
#    def __init__(self, port = DEFAULT_FILE, timeout = DEFAULT_TIMEOUT):
#        #initialize and configure serial port class
#        self.file_ptr = port
#        self.tty = None
#        self.setTimeout(timeout)
#
#    def is_open(self):
#        return not self.tty.closed
#
#    def get_port(self):
#        return self.tty.name
#
#    def set_port(self, port):
#        self.tty.port = port
#
#    def open_stream(self):
#        self.tty = open(self.file_ptr,'r')
#
#    def close_stream(self):
#        self.tty.close()
#
#    def write_block(self, stream, blocksize):
#        print debug_msg.TBD_STR
#
#    def read_block(self, blocksize):
#        print debug_msg.TBD_STR
#
#    def word_received(self):
#        print debug_msg.TBD_STR
#
#    def read_all(self):
#        stream = self.tty.read()
#        return stream
#
#    def read_string(self):
#        stream = self.tty.readline()
#        return stream
#
#    def write_string(self, stream):
#        self.tty.write(stream)
#
#    def flush(self):
#        self.tty.flush()
#
#    def free(self):
#        self.tty.__del__()

"""@package docstring
Documentation for this module.

Only TCP implemntend for the moment, ActiveX can be extended to GPIB
"""
class ActiveXLeCroyPort():

    def __init__(self, protocol = "TCPIP", address = None, port = None, 
                 timeout = DEFAULT_TIMEOUT):
        """The constructor.
            initialize and configure activeX port class
        """
        self.protocol = protocol
        self.address = address
        self.port = port
        self.timeout = timeout
        # Load ActiveDSO control
        self.tty = win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
        self.set_timeout(timeout)

    def about_port(self):
        """ Present the ActiveX control's About box"""
        self.tty.AboutBox()

    def is_open(self):
        """Documentation for a method."""
        print debug_msg.TBD_MSG

    def get_address(self):
        """Documentation for a method."""
        return self.address

    def get_timeout(self):
        """Documentation for a method."""
        return self.timeout

    def set_timeout(self, timeout):
        """Documentation for a method."""
        print timeout
        print debug_msg.TBD_MSG

    def open_stream(self):
        """Substitute your choice of IP address here"""
        self.tty.MakeConnection("IP:"+self.address)

    def close_stream(self):
        """Documentation for a method."""
        self.tty.Disconnect()

    def set_timeout_ms(self, timeout):
        """Documentation for a method."""
        print timeout
        print debug_msg.TBD_MSG

    def read_block(self, block_size):
        """Documentation for a method."""
        stream = self.tty.ReadString(block_size)
        return stream

    def write_string(self, stream):
        """Documentation for a method."""
        self.tty.WriteString(stream, 1)
        time.sleep(DEFAULT_WAIT_TIME)

    def query(self, cmd, read_buffer_size = DEFAULT_BUFFER_SIZE):
        """Documentation for a method."""
        self.write_string(cmd)
        return self.read_block(read_buffer_size)
        
"""Documentation for a class.

More details.
"""
class PyVisaPort():
    """ """
    def __init__(self, protocol = "GPIB", address = None, board = 0, 
                  timeout = DEFAULT_TIMEOUT):
        self.protocol = protocol
        self.address = address
        self.board = board
        self.timeout = timeout
        self.tty = visa.instrument('GPIB'+str(board)+'::'+str(address))
        self.set_timeout(timeout)

    def is_open(self):
        """Documentation for a method."""
        print debug_msg.TBD_MSG

    def get_address(self):
        """Documentation for a method."""
        return self.address

    def get_timeout(self):
        """Documentation for a method."""
        return self.timeout

    def set_timeout(self, timeout):
        """Documentation for a method."""
        self.timeout = timeout
        self.tty.timeout = timeout

    def open_stream(self):
        """Documentation for a method."""
        print debug_msg.TBD_MSG

    def close_stream(self):
        """Documentation for a method."""
        print debug_msg.TBD_MSG

    def set_timeout_ms(self, obj, timeout):
        """Documentation for a method."""
        print debug_msg.TBD_MSG

    def read_string(self):
        """Documentation for a method."""
        stream = self.tty.read()
        return stream

    def write_string(self, stream):
        """Documentation for a method."""
        self.tty.write(stream)
        time.sleep(DEFAULT_WAIT_TIME)

    def query(self, cmd, read_buffer_size = DEFAULT_BUFFER_SIZE):
        """Documentation for a method."""
        self.write_string(cmd)
        return self.read_string()

"""Documentation for a function.

More details.
"""
def main():
    #initialise and open_stream port
    Istream = PySerialPort(protocol = "SERIAL", port = 4, timeout = DEFAULT_TIMEOUT, baud = 1200)
    print Istream.is_open()
    Istream.open_stream()
    Istream.write_string('vDM?\r')
    time.sleep(1)
    print Istream.tty.inWaiting()
#    
#    Istream.write_string('>\r')
#    time.sleep(1)
#    print Istream.tty.inWaiting()
#    
#    Istream.write_string('>Iv\r')
#    time.sleep(1)
    print Istream.read_all()
#    
    Istream.close_stream()
#    
#    #initialise and open_stream port
#    Istream = ActiveXLeCroyPort(protocol = "TCPIP", address = "192.168.1.10", 
#                                 port = None, timeout = DEFAULT_TIMEOUT)
#    print Istream.is_open()
#    Istream.about_port()
#    Istream.open_stream()
#    Istream.write_string("*IDN?")
#    print Istream.read_block(1000)
#    print 'Test query'
#    print Istream.query("*IDN?", 1000)
#    time.sleep(1)
#    
#    Istream.close_stream()
#    
#    #Create connection to instrument
#    scope_protocol = 'GPIB'
#    scope_board = 0
#    scope_address = 10
#    for i in range(10):
#        Istream = PyVisaPort(scope_protocol, scope_address, scope_board, DEFAULT_TIMEOUT)
#        Istream.write_string("*IDN?")
#        time.sleep(1)
#        print Istream.read_string()
#        time.sleep(1)
#        print Istream.query("*IDN?", 1000)


if __name__ == "__main__":
    main()



