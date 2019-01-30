# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 17:19:58 2012

@author: tinix84
"""
from __future__ import division
import os, csv
import re
import matplotlib.pyplot as plt

import sys
sys.path.append('../lib/')
from lrf_histogram import *

def main():
    target_distance = 7000
    #get name of current directory
    base_name = os.path.realpath('./').split('\\')[-1]
    try:
        os.remove('./folder_summary.txt')
    except WindowsError:
        pass
    fid_wr = open('./folder_summary.txt', 'a')
    fid_wr.write("%s\n" % base_name)
    fid_wr.close()
    plt.figure(figsize=(8, 6))

    read_filename = '../Mxtest2.txt'
    #read_filename = '../Mx120508193220.txt'    
    fid_rd = open(read_filename,'r')
    foo = fid_rd.read()
    stream = re.findall(r'[a-zA-Z0-9_\-\n\r<%\*]', foo)

    comment_list = extract_comment(fid_rd)
    fid_rd.close()
    mx_cmd_info = MxCommand()
    mx_cmd_info = load_data_from_mxstream(mx_cmd_info, stream)
    measure_list = do_report_mx(read_filename, mx_cmd_info, target_distance)
    # Creates the plot.  No need to save the current figure.
    print mx_cmd_info['Histogram']['histo_size']
    print mx_cmd_info['Apd']['noise_apd_size']
    print mx_cmd_info['swVersion'] 
    plt.plot(mx_cmd_info['Histogram']['raw_data'])

    ydata = np.array(mx_cmd_info['Histogram']['raw_data'])
    xdata = np.arange(ydata.size)
    xydata = np.vstack((xdata, ydata))
    plt.show()

if __name__ == "__main__":
    main()