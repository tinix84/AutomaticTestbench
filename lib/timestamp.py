# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 11:22:26 2013

@author: tricc
"""
import datetime

def timeStamped(fname, fmt='%Y%m%d%H%M%S{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

if __name__ == '__main__' :
    
    time_filename = timeStamped('_')
    print time_filename