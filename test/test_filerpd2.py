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
flash_page_size = 256

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
        time.sleep(.01)
        read_str = myLRF.port.read_block(flash_page_size+1)
        bin_read_image = bin_read_image + hexstr2intlist(read_str[0:-1])
        address = address + flash_page_size
        
    if remaining_bytes:      
        print "ReadAddress last burst 0x%x" % address
        start_address_hex = int2hexstring(address, 6)
        read_length_hex = int2hexstring(remaining_bytes, 6)
        cmd=">Z95"+"\r"+start_address_hex+read_length_hex   
        myLRF.port.write_string(cmd)
        time.sleep(.01)
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
            time.sleep(.01)
            write_byte = fid_prog.read(1)
            #convert string UTF-16 to int16
            write_byte = int(write_byte.encode('hex'), 16)
            #cmd = cmd + int2hexstring(write_byte, 2)
            flip_write_byte = reverse_bit_order(write_byte, 8)
            myLRF.port.write_block(chr(flip_write_byte), 1)
        time.sleep(.01)
        res=myLRF.port.read_all()
        while (res != "<"):
            res=myLRF.port.read_all()            
        print res
        address = address + flash_page_size
        #time.sleep(.1)
        
    if prog_remaining_bytes:
        print "WriteAddress last burst 0x%x" % address
        start_address_hex = int2hexstring(address, 6)
        read_length_hex = int2hexstring(prog_remaining_bytes, 6)
        time.sleep(.01)
        cmd=">Z98"+"\r"+start_address_hex+read_length_hex
        myLRF.port.write_string(cmd)
        for j in range(prog_remaining_bytes):
            time.sleep(.01)
            write_byte = fid_prog.read(1)
            #convert string UTF-16 to int16
            write_byte = int(write_byte.encode('hex'), 16)
            #cmd = cmd + int2hexstring(write_byte, 2)
            flip_write_byte = reverse_bit_order(write_byte, 8)
            myLRF.port.write_block(chr(flip_write_byte), 1)
        time.sleep(.01)
        res=myLRF.port.read_all()
        while (res != "<"):
            res=myLRF.port.read_all()
        print res
        
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
    end_address = 0x000300
    
    myport = generic_port.PySerialPort(5,TIME_OUT,57600)
    dbgport = generic_port.PySerialPort(20,TIME_OUT,57600)
    myLRF = MBModC.MBModC(myport, TIME_OUT, sample_frequency)

    myLRF.port.open_stream()
    #Start the downloader.
    #myLRF.port.write_string(">Z98\r\n")
    #COMMAND FOR COPY/PASTE INTO SIMPLETERM:
    #ReadFirstPage
    #>Z95\r\00\00\00\00\01\00
    #WriteFirst4Bytes0x00 This writes 4 bytes of the page setting them to 0x00
    #>Z98\r\00\00\00\00\00\04\00\00\00\00
    #WriteFirst4Bytes0xFF This writes 4 bytes of the page setting them to 0xFF
    #>Z98\r\00\00\00\00\00\04\FF\FF\FF\FF
    #EraseBulkFlash
    #>Z96\r
    #LoadNewFPGAConfiguration
    #>Z94\r
    #myLRF.port.write_string(">Z95\r\x00\x00\x00\x00\x01\x00")
    time.sleep(.5)
    
    #print reverse_bit_order(65,8)


    fid_prog = open(prog_filename, 'rb')
    writeEPCSflash(myLRF, fid_prog, start_address, end_address)
    #time.sleep(2)
    #myLRF.port.read_all()
    
    bin_flip_read_image = []     
    start_time = time.time()
    bin_read_image = readEPCSflash(myLRF, start_address, end_address)
    print "Done! Time elapsed:"
    print time.time() - start_time, "seconds"
    
    for bin_value in bin_read_image:
        bin_flip_value = reverse_bit_order(bin_value, 8)
        bin_flip_read_image.append(bin_flip_value)
    #print read_flash_str
    #print bin_read_image
    rx_len=len(bin_read_image)
    myLRF.port.close_stream()
    fid_prog.close()
    
    fid_prog = open(prog_filename, 'rb')
    bin_file_image = []
    foo_str = fid_prog.read(rx_len)   
    for item in foo_str:
        bin_value = int(item.encode('hex'), 16)
        bin_file_image.append(bin_value)
 
#    print "Flash contents flipped:"
#    print bin_flip_read_image
#    print "Original file:"
#    print bin_file_image
    
    error=0
    error_position = []
    #compare files
    print "rx_len is %s" % rx_len
    
    for item in xrange(rx_len):
        if bin_file_image[item] != bin_flip_read_image[item]:
            error = error + 1
            error_position.append(item)
    
    print "the error number is %s" % error
    
    if error != 0:        
        print "the error number is %s" % error
        print "the error position is %s" % error_position
      
    fid_wr = open('../read_rpd_epcs16.rpd', 'wb')
    for item in bin_read_image:
        fid_wr.write(chr(item))
    fid_wr.close()
    fid_prog.close()
    