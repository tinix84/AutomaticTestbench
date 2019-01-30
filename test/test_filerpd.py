# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 16:43:33 2013

@author: tricc
"""

import sys
sys.path.append('../include')
sys.path.append('../dev')
sys.path.append('../utility')
import time
#import asmod

import MBModC
import generic_port
#import fs


DEFAULT_TIME_OUT = 30
byte_per_page = 256
STX = 0x0F
ETX = 0x04
DLE = 0x05

flash_page_size = 256

#Sends the command and receives the response. Tries multiple times,
#if the receive is not successful.
def queryFL(LRFobj, command):
	sendCommandFL(LRFobj, command)
	command=ReadCommandFL(LRFobj)
    
#Capsulizes the command to packet and sends it to the serial port.
#<param name="command"></param>
def sendCommandFL(LRFobj, command):

  #Create command array.
  packet = []
  packet.append(STX) #<STX>, start of text
  packet.append(STX) #<STX>, start of text

  #Append the command with DLEs as needed.
  #DLE - Data Link Escape character (0x05)
  for b in command:
    if (b == STX or b == ETX or b == DLE):
      packet.append(DLE); #Escape next byte.
    packet.append(b)

  #Calculate and append the checksum. DLE if needed.
  #It is the two's complement of the least significant byte of 
  #the sum of all data bytes.
  sum = 0
  for b in command: 
    sum += b
    checksum = (~sum + 1)%255
  if (checksum == STX or checksum == ETX or checksum == DLE):
    packet.append(DLE) #Escape next byte.
  packet.append(checksum)

  #End of packet.
  packet.append(ETX); #end of text byte

  #Write it to the port.
  LRFobj.port.write_block(packet, len(packet))

#Reads command from the serial port.
#If the command is not available in 1 second, the method throws an exception.
#<returns>Read command</returns>
def ReadCommandFL(LRFobj):
  #Command plus one checksum byte at the end. No DLEs.
  command = []
  temp = []
  state = "Start"
  success = False
  
  temp = LRFobj.read_all()
  
  for b in temp:
      if state == "Start":
        if (b == STX):
          state = "AfterFirstStx"
          
      elif state == "AfterFirstStx":
        if (b == STX):
          state = "CommandBody"
        else:
          state = "Start"
          
      elif state == "CommandBody":
        if (b == DLE):
          state = "CommandBodyEscaped"
        elif (b == ETX):
            success = True
        else:
            command.append(b)
      elif state == "CommandBodyEscaped":
          command.append(b)
          state = "CommandBody"
      else:
          pass
  
  #Check the checksum.
  receivedChecksum = command[len(command) - 1] #Store received checksum.
  command.RemoveAt(command.Count - 1) #Remove the checksum from the message.
  #It is the two's complement of the least significant byte of 
  #the sum of all data bytes.
  sum = 0;
  for b in command:
    sum += b;
  calculatedChecksum = (~sum + 1)%255
  if (receivedChecksum != calculatedChecksum):
    print ("Checksum error while reading command.\n")
    print ("Received checksum: %02x.\n"% receivedChecksum)
    print ("Calculated checksum: %02x.\n"% calculatedChecksum)

  return success, command
  
#Builds up the connection to the micro controller, switches the speed 
#to 9k6 and checks if the connection is working.
def ConnectFPGA(LRFobj):
  
  LRFobj.port.open_stream() 
  #Start the downloader.
  LRFobj.port.write_string(">Z98\r\n")
  time.sleep(.5)

  #Check if the DSP started the boot loader successfully.
  response = LRFobj.port.read_all()
  print response
  
  
  
#  if (not(">zB8" in response)):
#    print "DSP UnableToConnect"
#    return False
    

  #If we receive ACK(<), the boot loader is understand the command.
  #If we receive NACK(!), the boot loader is not understand the command.
  #If we receive nothing in 1 second, the boot loader is not started.
  if (("!" in response)):
    print "cmd unrecognized"
  elif (not("<" in response)):
    print "cmd recognized"

#  #Get boot loader info.
#  response = LRFobj.queryFL([0x00, 0x02])
#  #we must wait for a timeout to let the uC to check the silicon ID
#  time.sleep(.1)
#  if (len(response) != 4 or response[0] != 0x00 or response[1] != 0x02):
#    print  "Boot loader info command failed."
#
#  silicon_id = response[2]
  
  #OK, boot loader started.
  return True
  
def reverse_bit_order(n, width):
    b = '{:0{width}b}'.format(n, width=width)
    return int(b[::-1], 2)

def hexstr2intlist(hex_string):
    int_list = [] 
    for item in hex_string:
        int_item = int(item.encode('hex'), 16)
        int_list.append(int_item)
    return int_list

def value2bytearray(value):
    pass
    
def int2hexstring(int_value, width):
   encoded = format(int_value, 'x')
   encoded = encoded.zfill(width)
   return encoded.decode('hex')
   
def readEPCSflash(LRFdev, start_address, end_address):
    prog_len = end_address - start_address
    number_of_pages = prog_len/flash_page_size
    remaining_bytes = prog_len % flash_page_size
    print "Number of flash pages to read is %d" % number_of_pages  
    
    bin_read_image = []
    address = 0
    
    myLRF.port.flush()
    
    for page in xrange(number_of_pages):
        print "ReadAddress 0x%x" % address
        start_address_hex = int2hexstring(address, 6)
        read_length_hex = int2hexstring(flash_page_size, 6)
        cmd=">Z95"+"\r"+start_address_hex+read_length_hex   
        myLRF.port.write_string(cmd)
        time.sleep(.1)
        read_str = myLRF.port.read_block(flash_page_size+1)
        bin_read_image = bin_read_image + hexstr2intlist(read_str[0:-1])
        address = address + flash_page_size
        
    if remaining_bytes:      
        print "ReadAddress last burst 0x%x" % address
        start_address_hex = int2hexstring(address, 6)
        read_length_hex = int2hexstring(remaining_bytes, 6)
        cmd=">Z95"+"\r"+start_address_hex+read_length_hex   
        myLRF.port.write_string(cmd)
        time.sleep(.1)
        read_str = myLRF.port.read_block(remaining_bytes+1)
        bin_read_image = bin_read_image + hexstr2intlist(read_str[0:-1])
        
    return bin_read_image
    
def writeEPCSflash(LRFdev, fid_prog, start_address, end_address):
    prog_len = end_address - start_address
    prog_page_number = prog_len/flash_page_size
    prog_remaining_bytes = prog_len % flash_page_size
    print "Number of flash pages to write is %d" % prog_page_number  
    print "Number of bytes to write is %d" % prog_remaining_bytes  
    
    bin_read_image = []
    address = 0
    
    for page in xrange(prog_page_number):
        print "WriteAddress 0x%x" % address
        start_address_hex = int2hexstring(address, 6)
        read_length_hex = int2hexstring(flash_page_size, 6)
        cmd=">Z98"+"\r"+start_address_hex+read_length_hex
        myLRF.port.write_string(cmd)
        for j in range(flash_page_size):
            time.sleep(.0001)
            write_byte = fid_prog.read(1)
            #convert string UTF-16 to int16
            write_byte = int(write_byte.encode('hex'), 16)
            #cmd = cmd + int2hexstring(write_byte, 2)
            flip_write_byte = reverse_bit_order(write_byte, 8)
            myLRF.port.write_block(chr(flip_write_byte), 1)
        res=myLRF.port.read_all()
        print res
        while (res != "<"):
            res=myLRF.port.read_all()            
        address = address + flash_page_size
        time.sleep(.5)
        
    if prog_remaining_bytes:
        print "WriteAddress last burst 0x%x" % address
        start_address_hex = int2hexstring(address, 6)
        read_length_hex = int2hexstring(prog_remaining_bytes, 6)
        time.sleep(.1)
        cmd=">Z98"+"\r"+start_address_hex+read_length_hex
        myLRF.port.write_string(cmd)
        for j in range(prog_remaining_bytes):
            time.sleep(.0001)
            write_byte = fid_prog.read(1)
            #convert string UTF-16 to int16
            write_byte = int(write_byte.encode('hex'), 16)
            #cmd = cmd + int2hexstring(write_byte, 2)
            flip_write_byte = reverse_bit_order(write_byte, 8)
            myLRF.port.write_block(chr(flip_write_byte), 1)
        res=myLRF.port.read_all()
        print res
        while (res != "<"):
            res=myLRF.port.read_all()        
        
    return bin_read_image
    

if __name__ == '__main__' :

    sample_frequency = 100e6

    TIME_OUT = 10000

    prog_filename = '../LRF_main.rpd'
    test_prog_filename = '../TestPatternLRF_main.rpd'
    map_filename = '../LRF_map.rpd'
    read_flash_filename = '../readLRFflash.rpd'

    #these should be read from map file
    start_address = 0x0000000
    #end_address = 0x0007CB87
    end_address = 0x000200
    
    myport = generic_port.PySerialPort(5,TIME_OUT,57600)
    dbgport = generic_port.PySerialPort(20,TIME_OUT,57600)
    myLRF = MBModC.MBModC(myport, TIME_OUT, sample_frequency)

    myLRF.port.open_stream()
    #Start the downloader.
    #myLRF.port.write_string(">Z98\r\n")
    #>Z95\00\00\00\00\01\00\r\n
    #>Z98\00\00\00\00\00\02\r\n\00\00\00\00
    #>Z98\00\00\00\00\00\04\0D\0A\01\02\03\04
    #>Z98\00\00\00\00\00\04\0D\FF\FF\FF\FF\FF
    #myLRF.port.write_string(">Z95\x00\x00\x00\x00\x10\x00\r\n")
    time.sleep(.5)
    
    #print reverse_bit_order(65,8)


    fid_prog = open(prog_filename, 'rb')
    #writeEPCSflash(myLRF, fid_prog, start_address, end_address)
    #time.sleep(2)
    #myLRF.port.read_all()
    
    bin_flashcontents = readEPCSflash(myLRF, start_address, end_address)
    #print read_flash_str
    #print bin_read_image
    myLRF.port.close_stream()
    
    rx_len=len(bin_flashcontents)
    fid_prog.seek(0)
    foo_str = fid_prog.read(rx_len)   
    
    bin_flash_image = []
    
    for item in foo_str:
        bin_value = int(item.encode('hex'), 16)
        bin_flash_image.append(bin_value)

    bin_flip_flashcontents = [] 
    
    for bin_value in bin_flashcontents:
        bin_flip_value = reverse_bit_order(bin_value, 8)
        bin_flip_flashcontents.append(bin_flip_value)
    
    print "Flash contents:"
    print bin_flip_flashcontents
    print "Original file flipped:"
    print bin_flash_image
    
    error=0
    error_position = []
    #compare files
    print "rx_len is %s" % rx_len
    
    for item in xrange(rx_len):
        if bin_flash_image[item] != bin_flip_flashcontents[item]:
            error = error + 1
            error_position.append(item)
    
    print "the error number is %s" % error
    
    if error != 0:        
        print "the error number is %s" % error
        print "the error position is %s" % error_position
  
    fid_wr = open('../read_rpd_epcs16.rpd', 'wb')
    for item in bin_flashcontents:
        fid_wr.write(chr(item))
    fid_wr.close()
    