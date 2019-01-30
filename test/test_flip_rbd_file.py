# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 19:04:13 2013

@author: tricc
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 16:43:33 2013

@author: tricc
"""

import sys
sys.path.append('../include')
sys.path.append('../dev')
sys.path.append('../utility')

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

if __name__ == '__main__' :


    prog_filename = '../LRF_main.rpd'
    prog_filename_byte_flip = '../LRF_main_flip.rpd'
    
    fid_rd = open(prog_filename, 'rb')
    bin_read_image = fid_rd.read()
    
    file_size=len(bin_read_image)
    
    bin_flash_image = []
    bin_flip_read_image = [] 
    
    for item in bin_read_image:
        bin_value = int(item.encode('hex'), 16)
        bin_flash_image.append(bin_value)
        bin_flip_value = reverse_bit_order(bin_value, 8)
        bin_flip_read_image.append(bin_flip_value)
    
    #print bin_flash_image
    #print bin_flip_read_image
      
    
    fid_wr = open(prog_filename_byte_flip, 'wb')
    for item in bin_flip_read_image:
        fid_wr.write(chr(item))
    fid_wr.close()
    
