# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 13:08:37 2012

@author: tricc
"""
import sys
sys.path.append('../include/')
import errcode
import fs

EPCS_device = 0
RPD_file_size = 0

## Documentation for a function.
# Name:    as_program
# Descriptions: Get programming file size, parse through every single byte and dump to
# parallel port. FPGA access to the EPCS is disable when the programming starts.
def as_program(LRFModCobj):

    status = 0

    # Disable FPGA access to EPCS
    status = as_program_start(LRFModCobj)
    if ( status != errcode.CB_OK  ):
        return status

#    # Read EPCS silicon ID
#    status = as_silicon_id(LRFModCobj)
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    # EPCS Bulk Erase
#    status = as_bulk_erase( )
#    if ( status != errcode.CB_OK  ):
#        return status

    # Start EPCS Programming
    status = as_prog(LRFModCobj)
    if ( status != errcode.CB_OK  ):
        return status

#    # Start EPCS Verifying
#    status = as_verify( file_id, file_size )
#    if ( status != errcode.CB_OK  )
#        return status

    # Enable FPGA access to EPCS
    status = as_program_done()
    if ( status != errcode.CB_OK  ):
        return status

    status = as_close(LRFModCobj)
    if ( status != errcode.CB_OK  ):
        return status

    return errcode.CB_OK

### Documentation for a function.
## Name:    as_ver
## Descriptions: Verify EPCS data
#def as_ver( file_path, epcsDensity ):
#    status = 0
#    file_id = 0
#    file_size = 0
#
#    # Open RPD file for verify
#    status = as_open(LRFModCobj)
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    # Disable FPGA access to EPCS
#    status = as_program_start()
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    # Read EPCS silicon ID
#    status = as_silicon_id(LRFModCobj)
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    # Start EPCS Verifying
#    status = as_verify(LRFModCobj)
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    # Enable FPGA access to EPCS
#    status = as_program_done()
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    status = as_close(LRFModCobj)
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    return errcode.CB_OK

## Documentation for a function.
# Name:    as_open
# Descriptions: Open all devices to program the FPGA
def as_open(LRFModCobj):

    status = 0

    status, LRFModCobj.EPCSwritefid = fs.fs_open(LRFModCobj.EPCSwritefile, "rb")
    if ( status != errcode.CB_OK  ):
        return status



    status, LRFModCobj.EPCSwritefile_size = fs.fs_size(LRFModCobj.EPCSwritefid)
    if ( status != errcode.CB_OK  ):
        return status

    return errcode.CB_OK

## Documentation for a function.
# Name:    as_open
# Descriptions: Open all devices to program the FPGA
def as_close(LRFModCobj):

    status = 0

    status, LRFModCobj.EPCSwritefid = fs.fs_close(LRFModCobj.EPCSwritefile, "rb")
    if ( status != errcode.CB_OK  ):
        return status

    if not(LRFModCobj.port.is_open()):
        LRFModCobj.port.open_stream()
        LRFModCobj.port.write_string("<\r")

    return errcode.CB_OK

### Documentation for a function.
## Name:    as_read
## Descriptions: Get EPCS data and save in a file
#def as_read(LRFModCobj):
#    status = 0
#    file_id = 0
#    file_size = 0
#
#    if not(LRFModCobj.port.is_open()):
#        LRFModCobj.port.open_stream()
#
#    # Open RPD file for to store EPCS data
#    status, file_id = fs_open( file_path, "w+b")
#    if ( status != errcode.CB_OK ):
#        return status
#
#    # Enable FPGA access to EPCS
#    status = as_program_start()
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    # Read EPCS silicon ID
#    status = as_silicon_id(DEV_READBACK, epcsDensity)
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    # Start EPCS Readback
#    status = as_readback(file_id)
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    # Enable FPGA access to EPCS
#    status = as_program_done()
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    status = as_close( file_id )
#    if ( status != errcode.CB_OK  ):
#        return status
#
#    return errcode.CB_OK

## Documentation for a function.
# Name:    as_program_start
# Descriptions:
def as_program_start(LRFModCobj):
    # Drive NCONFIG to reset FPGA before programming EPCS ( NCONFIG, 0 )
    # Drive NCE to disable FPGA from accessing EPCS ( NCE, 1 )
    # Drive NCS to high when not acessing EPCS ( NCS, 1 )
    LRFModCobj.port.write_string(">Ud\r")
    return errcode.CB_OK

## Documentation for a function.
# Name:    as_program_done
# Descriptions:
def as_program_done(LRFModCobj):
    # Drive NCE to enable FPGA ( NCE, 0 )
    # Drive NCONFIG from low to high to reset FPGA ( NCONFIG, 1 )
    # Drive NCS to high when not acessing EPCS ( NCS, 1 )
    LRFModCobj.port.write_string(">as_program_done\r")
    return errcode.CB_OK

def as_prog(LRFModCobj):

    page = 0
    one_byte = 0
    EPCS_Address =0
    StatusReg =0
    i = 0
    j = 0        
    status = 0
    bal_byte = 0
    byte_per_page = 256

    print "\nInfo: Start programming process" 
    page = LRFModCobj.EPCSwritefile_size/256
    print "\nInfo: page %d" % page
    bal_byte = LRFModCobj.EPCSwritefile_size%256
    print "\nInfo: bal_byte %d" % page
    
    #if there is balance after divide, program the balance in the next page
    if(bal_byte != 0):
        page=page+1
    
    print "\nInfo: page %d" % page
    
    # ( NCS, 0 )
    # as_program_byte_msb( AS_WRITE_ENABLE )
    # ( NCS, 1 )
    LRFModCobj.port.write_string(">as_prog1\r")

    print "\nInfo: Programming..." 
    
    for i in range(page):      
       command = ">as_prog %d\r" % page
        # ( NCS, 0 )
        # as_program_byte_msb( AS_WRITE_ENABLE )
        # ( NCS, 1 ) 
#        ( NCS, 0 )
#        as_program_byte_msb( AS_PAGE_PROGRAM )
#        EPCS_Address = i*256
#        as_program_byte_msb( ((EPCS_Address & 0xFF0000)>>16));
#        as_program_byte_msb( ((EPCS_Address & 0x00FF00)>>8) );
#        as_program_byte_msb( EPCS_Address & 0xFF);
       LRFModCobj.port.write_string(command)
        
        #if the last page has has been truncated less than 256:
       if((i == (page - 1)) and (bal_byte != 0)):    
            byte_per_page = bal_byte
            
       for j in range(byte_per_page):

            #read one byte
            status, one_byte = fs.fs_read( LRFModCobj.EPCSwritefid)
            if ( status != errcode.CB_OK ):
                return status

            #Progaram a byte
            LRFModCobj.port.write_block(one_byte, 1)
            
            #bb_write( NCS, 1 )
            #status = bb_flush()
            #bb_write( NCS, 0 )
            LRFModCobj.port.write_string("\rmsbAS_READ_STATUS")
            #status = bb_flush()
            LRFModCobj.port.write_string("\rmsbStatusReg")
            #while((StatusReg & 0x01))
            #bb_write( NCS, 1 )
            #status = bb_flush()
            

    print "Info: Programming successful\n"

    #=========== Page Program command End==========

    return errcode.CB_OK