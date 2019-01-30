# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 17:38:57 2014

@author: 212334547
"""
import sys

class MyLogOutput():
    def __init__(self, logfile):
        self.stdout = sys.stdout
        self.log = open(logfile, 'w')

    def write(self, text):
        self.stdout.write(text)
        self.log.write(text)
        self.log.flush()

    def close(self):
        self.stdout.close()
        self.log.close()
        
if __name__ == '__main__' :
    sys.stdout = MyLogOutput(self.log_filename)
