# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 13:08:37 2012

@author: tricc
"""
import sys
sys.path.append('../include/')
import errcode


## Documentation for a function.
# Name:	fs_open  
# Descriptions: Open programming file	
def fs_open( filename, mode ):
	try:
		fid = open( filename, mode )
	except IOError:
		print "Error: Could not open file: \"%s\"!\n"% filename
		return fid, errcode.CB_FS_OPEN_FILE_ERROR
	else:
		print "Info: Programming file: \"%s\" opened.\n"% filename
		return errcode.CB_OK, fid

## Documentation for a function.
# Name:	fs_close  
# Descriptions: Close file	
def fs_close( file_id ):
	try:
		file_id.close()
	except IOError:
		print "Error: Could not close file!\n"
		return errcode.CB_FS_CLOSE_FILE_ERROR
	else:
		return errcode.CB_OK

## Documentation for a function.
# Name:	fs_size  
# Descriptions: check file size
def fs_size( file_id ):
	try:
		file_id.seek(0,2)
	except IOError:
		print "Error: End of file could not be located!"
		return errcode.CB_FS_SIZE_EOF_NOT_FOUND
	else:
	    size = file_id.tell()
      file_id.seek(0)
	return errcode.CB_OK, size

## Documentation for a function.
# Name:	fs_read  
# Descriptions: read a byte from file
def fs_read( file_id ):
	try:
		data = file_id.read(1)
	except IOError:
		print "Error: Could not read data from file!"
		return errcode.CB_FS_SIZE_EOF_NOT_FOUND
	else:
		return errcode.CB_OK, data
		
## Documentation for a function.
# Name:	fs_write  
# Descriptions: write a byte to file
def fs_write( file_id, data ):
	try:
		file_id.write(chr(data))
	except IOError:
		print "Error: file could not be written!"
		return errcode.CB_FS_SIZE_EOF_NOT_FOUND
	else:
		return errcode.CB_OK
		
## Documentation for a function.
# Name:	fs_rewind  
# Descriptions: Repositions the file pointer to the beginning of a file
def fs_rewind( file_id ):
	try:
		file_id.seek(0)
	except IOError:
		print "Error: End of file could not be located!"
		return errcode.CB_FS_SIZE_EOF_NOT_FOUND
	else:
		return errcode.CB_OK