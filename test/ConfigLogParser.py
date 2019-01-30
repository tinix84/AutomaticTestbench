# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 14:32:47 2013

@author: 212334547
"""

#!/usr/bin/env python
## {{{ http://code.activestate.com/recipes/534109/ (r8)
from __future__ import division
import os, csv
#import stat
#import array
import re
import numpy as np
#from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
#import matplotlib.collections as collections
from datetime import datetime
#import AnnotateFinder
#import pylab
#import matplotlib

def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    print 'onpick points:', zip(xdata[ind], ydata[ind])


class UPSLog(object):
    def __init__(self):
        self.alarmInfo={}
        self.alarmInfo['time'] = []
        self.alarmInfo['value'] = []
        self.bypassVoltage={}
        self.bypassVoltage['time'] = []
        self.bypassVoltage['value'] = []
        self.inputVoltage={}
        self.inputVoltage['time'] = []
        self.inputVoltage['value'] = []
        self.bypassFrequency={}
        self.bypassFrequency['time'] = []
        self.bypassFrequency['value'] = []
        self.bypassCurrent={}
        self.bypassCurrent['time'] = []
        self.bypassCurrent['value'] = []
        self.bypassPower={}
        self.bypassPower['time'] = []
        self.bypassPower['value'] = []
        self.batteryVoltage={}
        self.batteryVoltage['time'] = []
        self.batteryVoltage['value'] = []
        self.batteryCurrent={}
        self.batteryCurrent['time'] = []
        self.batteryCurrent['value'] = []
        self.batteryStatus={}
        self.batteryStatus['time'] = []
        self.batteryStatus['value'] = []


def getUpsAlarmGroupA(stream):
    #round brackets (\d+) are important to recall number after
    pattern=re.compile(r'vAa(\d+)')
    match=pattern.search(stream)
    value = int(match.group(1))
    return value
    
    
def getUpsInputLineBads(stream):
	 pass
def getUpsBypassVoltage(stream):
	 pass
def getUpsBypassFrequency(stream):
	 pass
def getUpsBypassCurrent(stream):
	 pass
def getUpsBypassPower(stream):
	 pass
def getUpsOutputVoltage(stream):
	 pass
def getUpsOutputFrequency(stream):
	 pass
def getUpsOutputCurrent(stream):
	 pass
def getUpsOutputPower(stream):
	 pass
def getUpsOutputVA(stream):
	 pass
def getUpsOutputPercentLoad(stream):
	 pass
def getUpsOutputSource(stream):
	 pass

def getUpsBatteryVoltage(stream):
    #round brackets (\d+) are important to recall number after
    pattern=re.compile(r'vBU(\d+)')
    match=pattern.search(stream)
    return float(match.group(1))/10.0
    
def getUpsBatteryCurrent(stream):
	 pass
def getUpsBatteryTemperature(stream):
	 pass
def getUpsBatteryEstimatedMinutesRemaining(stream):
	 pass
def getUpsBatteryEstimatedChargeRemaining(stream):
	 pass
def getUpsBatteryStatus(stream):
    #round brackets (\d+) are important to recall number after
    pattern=re.compile(r'vBS(\d)')
    match=pattern.search(stream)
    return int(match.group(1))

def getUpsInputVoltage(stream):
    #round brackets (\d+) are important to recall number after
    pattern=re.compile(r'vI0U(\d+)')
    match=pattern.search(stream)
    return int(match.group(1))
    
def getUpsInputFrequency(stream):
	 pass
def getUpsInputCurrent(stream):
	 pass
def getUpsInputTruePower(stream):
	 pass
def getUpsInputVoltageMin(stream):
	 pass
def getUpsInputVoltageMax(stream):
	 pass

def main():
    
    vco3kLog = UPSLog()
    
    read_filename = './CEVO20A250000A000_422014_634PM_2.csv'

    
    # Read all lines using a list comprehension
    bank_records = [line for line in csv.reader(open(read_filename, 'rbU'), delimiter=';')]
    # Pop header from the start of the list and save it
    header = bank_records.pop(0) 
    print header
    
    # Open a new file object
    fp = open('postprocess.csv','a')
    
    bank_records_noheader=bank_records[9:-1]
    record=bank_records[9]
    print record
    start_logtime=datetime.strptime(record[0]+' '+record[1], '%I:%M:%S %p %m/%d/%Y')
    
    alarm_events = []
    # Now process and output the remaining lines. 
    for record in bank_records_noheader:
        # Do some basic processing and then write the data back out
        # Below, we use Python's built-in datetime library to reformat 
        # the Closing and Update dates. 
        # First, we use the "strptime" method to parse dates formatted 
        # as "23-Feb-11" into a native Python datetime object.
        # Then we apply the "strftime" method to the resulting datetime
        # object to create a date formatted as YYYY-MM-DD.
        #print record[0]
        logtime=datetime.strptime(record[0]+' '+record[1], '%I:%M:%S %p %m/%d/%Y')
        logdtime=(logtime-start_logtime).total_seconds()     
        
        #print record
        
        if record[2]=='vAa?':
            #print record[3]
#            value=getUpsAlarmGroupA(record[3])
#            vco3kLog.alarmInfo['time'].append(logdtime)
#            vco3kLog.alarmInfo['value'].append(value)
#            bin_value = "{0:032b}".format(value)
#            #print "%d, %s" % (logdtime, list(bin_value))     
#            #print "%d, %d" % (logdtime, value)
#            fp.writelines(["%s, %d, %d" % (logtime, logdtime, value)])
#            fp.write("\n")
            pass
            
        elif record[2]=='vIB?':
            getUpsInputLineBads(record[3])
        #match vP0U?, vP1U?, vP2U?
        elif re.search(r'vP\dU', record[2]):
            getUpsBypassVoltage(record[3])
        elif record[2]=='vPf?':
            getUpsBypassFrequency(record[3])
        elif re.search(r'vP\dI', record[2]):
            getUpsBypassCurrent(record[3])
        elif re.search(r'vP\dP', record[2]):
            getUpsBypassPower(record[3])
        elif re.search(r'vO\dU', record[2]):
            getUpsOutputVoltage(record[3])
        elif record[2]=='vOf?':
            getUpsOutputFrequency(record[3])
        elif re.search(r'vO\dI', record[2]):
            getUpsOutputCurrent(record[3])
        elif re.search(r'vO\dP', record[2]):
            getUpsOutputPower(record[3])
        elif re.search(r'vO\dV', record[2]):
            getUpsOutputVA(record[3])
        elif re.search(r'vO\dL', record[2]):
            getUpsOutputPercentLoad(record[3])
        elif record[2]=='vOs?':
            getUpsOutputSource(record[3])
        elif record[2]=='vBU?':
            value=getUpsBatteryVoltage(record[3])
            vco3kLog.batteryVoltage['time'].append(logdtime)
            vco3kLog.batteryVoltage['value'].append(value)
            print "%d, %f" % (logdtime, value)
            fp.writelines(["%s, %d, %f" % (logtime, logdtime, value)])
            fp.write("\n")
            pass
            
        elif record[2]=='vBI?':
            getUpsBatteryCurrent(record[3])
        elif record[2]=='vBT?':
            getUpsBatteryTemperature(record[3])
        elif record[2]=='vBt?':
            getUpsBatteryEstimatedMinutesRemaining(record[3])
        elif record[2]=='vBC?':
            getUpsBatteryEstimatedChargeRemaining(record[3])
        elif record[2]=='vBS?':
            value=getUpsBatteryStatus(record[3])
#            vco3kLog.batteryStatus['time'].append(logdtime)
#            vco3kLog.batteryStatus['value'].append(value)
            
        elif re.search(r'vI\dU', record[2]):
#            value=getUpsInputVoltage(record[3])
#            vco3kLog.inputVoltage['time'].append(logdtime)
#            vco3kLog.inputVoltage['value'].append(value)
#            print "%d, %d" % (logdtime, value)
            pass
            
        elif re.search(r'vI\df', record[2]):
            getUpsInputFrequency(record[3])
        elif re.search(r'vI\dI', record[2]):
            getUpsInputCurrent(record[3])
        elif re.search(r'vI\dP', record[2]):
            getUpsInputTruePower(record[3])
        elif re.search(r'vI\dl', record[2]):
            getUpsInputVoltageMin(record[3])
        elif re.search(r'vI\dh', record[2]):
            getUpsInputVoltageMax(record[3])
        else:
            #print "Unknown command"
            #print record[2]
            pass
    fp.close()
    
#    fig, ax = plt.subplots()
#    t1=np.array(vco3kLog.batteryStatus['time']) 
#    s1=np.array(vco3kLog.batteryStatus['value'])
#    t2=np.array(vco3kLog.batteryVoltage['time']) 
#    s2=np.array(vco3kLog.batteryVoltage['value'])       
#    print s1
#    ax.plot(t2, s2)
#
#    plt.show()
#    plt.grid()
#    plt.yticks([i for i in np.arange(np.ceil(np.min(s2)-1),np.ceil(np.max(s2)+1),1)])
    


if __name__ == "__main__":
    main()