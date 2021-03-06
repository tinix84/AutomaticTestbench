# -*- coding: utf-8 -*-
"""
Created on Mon Mar 05 12:41:33 2012

@author: tricc
"""


## {{{ http://code.activestate.com/recipes/534109/ (r8)
from __future__ import division
import os, csv
import stat
#import array
import re
import numpy as np
#from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
import peak_fit as pf

#constant definition for the position of the information into Mx command
WORD_NR_AVG_HISTO = 2
WORD_NR_STD_DEV = 3
WORD_NR_VAPD_DECR = 42
WORD_NR_SHOTS_NR = 43
WORD_NR_HP_DIST_OFFSET = 53
WORD_NR_LP_DIST_OFFSET = 56
WORD_NR_LAPD_DIST_OFFSET = 59
WORD_NR_DECR_DIST_FACT = 62
WORD_NR_HISTO_SIZE = 63
WORD_NR_NOISE_DISTR = 64


class MxCommand(object):
    def __init__(self):
        self.lrf_raw_stream = ''
        self.UcMsg = UcMsg()
         # Create an empty Histogram record
        self.Histogram = Histogram()
        # Create an empty offset setting record
        self.DistanceOffset = DistanceOffset()
        self.AllTargetInfo = {}
        self.AllTargetInfo['target1'] = TargetInfo()
        self.AllTargetInfo['target2'] = TargetInfo()
        self.AllTargetInfo['target3'] = TargetInfo()
        self.AllTargetInfo['target4'] = TargetInfo()
        self.AllTargetInfo['target5'] = TargetInfo()

        # Create an empty Apd record
        self.Apd = Apd()
        self.shots_nr = 0
        self.valid_target = 0

    def load_data_from_mxfile (self, stream_uint8= ""):
        try:
            #search char '*' into array
            uc_msg_len = np.where(stream_uint8 == 42)[0][0]
            histo_str = stream_uint8[uc_msg_len+2:]
            str_uc = stream_uint8[0:uc_msg_len+2].tostring()
            self.UcMsg.get_info(str_uc)
        except IndexError:
            histo_str = stream_uint8

        self.lrf_raw_stream = stream_uint8
        #Multiplication by 6 is due to the 24bits are trasmitter as a char
        #HistogramSize
        self.Histogram.avg = get_hex_param(histo_str, WORD_NR_AVG_HISTO)
        self.Histogram.std_dev = get_hex_param(histo_str, WORD_NR_STD_DEV)
        self.Histogram.std_dev_labview = self.Histogram.std_dev/4
        self.Histogram.std_dev_16 = self.Histogram.std_dev_labview/16

        #HistogramSize
        self.Apd.vapd_decr = get_hex_param(histo_str, WORD_NR_VAPD_DECR)
        self.shots_nr = get_hex_param(histo_str, WORD_NR_SHOTS_NR)
        #LRFOffset
        self.DistanceOffset.high_power = get_hex_param(histo_str,
                                                        WORD_NR_HP_DIST_OFFSET)
        self.DistanceOffset.low_power = get_hex_param(histo_str,
                                                       WORD_NR_LP_DIST_OFFSET)
        self.DistanceOffset.low_apd = get_hex_param(histo_str,
                                                     WORD_NR_LAPD_DIST_OFFSET)
        self.DistanceOffset.decr_dist_fact = get_hex_param(histo_str,
                                                          WORD_NR_DECR_DIST_FACT)

        # Histogram Size
        self.Histogram.histo_size = get_hex_param(histo_str, WORD_NR_HISTO_SIZE)
        histo_len = self.Histogram.histo_size
        # noise_distribution Size
        self.Apd.noise_apd_size = get_hex_param(histo_str, WORD_NR_NOISE_DISTR)
        apd_distr_len = self.Apd.noise_apd_size

        #variable definition after having read apd_distr_len and histo_len
        word_nr_status_word = 65+apd_distr_len
        word_nr_opt_apd_voltage = 66+apd_distr_len
        word_nr_apd_distr = range(65,80,1)
        word_nr_histo = range(67+apd_distr_len,66+apd_distr_len+histo_len,1)
        word_nr_peak1_dist_decunit = 68+apd_distr_len+histo_len
        word_nr_valid_peaks = 102+apd_distr_len+histo_len
        word_nr_sw_ver = 103+apd_distr_len+histo_len

        self.Apd.opt_apd_voltage = get_hex_param(histo_str,
                                                word_nr_opt_apd_voltage)
        self.Apd.status_word = int(get_dec_param(histo_str,
                                                 word_nr_status_word).tostring())
        self.Apd.noise_distribution = get_apd_noise_distribution(
            histo_str, word_nr_apd_distr[1], word_nr_apd_distr[-1])
        self.Histogram.raw_data = get_histogram_data(
            histo_str, word_nr_histo[0], word_nr_histo[-1])

        self.valid_target =get_hex_param(histo_str, word_nr_valid_peaks)
        self.SwVersion = get_hex_param(histo_str, word_nr_sw_ver)
        self.AllTargetInfo = get_all_target_info(
            histo_str, word_nr_peak1_dist_decunit, self.Histogram.std_dev_labview)


#choose the target based to the distance from a given target:
def choose_target_number(self, target_pos, blind_time=40):
    closer_distance = self.Histogram.histo_size
    closer_target = None
    for item in self.AllTargetInfo:
        distance = abs(target_pos - self.AllTargetInfo[item].peak_pos_off3580)
        if blind_time < self.AllTargetInfo[item].peak_pos_off3580 :
            if distance < closer_distance:
                closer_distance = distance
                closer_target = item

    print "closer target distance %s" % closer_distance
    return closer_target
    
#choose the target based to the distance from a given target(priority2) and max SNR(priority1):
def choose_higherSNRtarget(self, mx_cmd_info, target_pos, blind_time):
    higher_SNR = 0
    higherSNRtarget = None
    for item in self.AllTargetInfo:
        SNRtarget = self.AllTargetInfo[item].snr
        if blind_time < self.AllTargetInfo[item].peak_pos_off3580 :
            if SNRtarget > higher_SNR:
                higher_SNR = SNRtarget
                higherSNRtarget = item

    print "closer target distance %s" % higherSNRtarget
    return higherSNRtarget
    
#def get_dec_param(stream = [], start= 0, stop = start):
def get_dec_param(*arg):
    stream = arg[0]
    start = arg[1]
    if len(arg) < 3:
        stop = start #if not defined stop=start
    else:
        stop = arg[2]
    ##Multiplication by 6 is due to the 24bits are trasmitter as a char
    par = stream[6*start-6:6*stop]

    return par

#def get_hex_param(stream = [], start= 0, stop = start):
def get_hex_param(*arg):
    stream = arg[0]
    start = arg[1]
    if len(arg) < 3:
        stop = start
    else:
        stop = arg[2]
    ##Multiplication by 6 is due to the 24bits are trasmitter as a char
    par = hex2dec(stream[6*start-6:6*stop])

    return par

def get_histogram_data(stream, start, stop):
    histo = get_dec_param(stream, start, stop)
    histo_dec = []
    for item in range(0, len(histo), 6):
        histo_dec.append(hex2dec(histo[item:item+6]))

    return histo_dec

def get_apd_noise_distribution(stream, start, stop):
    apd_distr = get_dec_param(stream, start, stop)
    apd_distr_dec = []
    for item in range(0, len(apd_distr), 6):
        apd_distr_dec.append(hex2dec(apd_distr[item:item+6]))

    return apd_distr_dec

def get_target_info(stream, start, std_dev_labview):
    target = TargetInfo()
    target.peak_dist_unit = int((get_dec_param(stream, start)).tostring())
    target.peak_pos_off3580 = get_hex_param(stream, start+1)-3580
    target.peak_loc_avg = get_hex_param(stream, start+2)
    target.peak_tg_pk_after_rel = get_hex_param(stream, start+3)
    target.peak_tg_pk_after_abs = target.peak_loc_avg - \
                                    target.peak_tg_pk_after_rel
    target.peak_tg_pk_rel = get_hex_param(stream, start+4)
    target.peak_tg_pk_abs = target.peak_loc_avg-target.peak_tg_pk_rel
    target.peak_tg_pk_before_rel = get_hex_param(stream, start+5)
    target.peak_tg_pk_before_abs = target.peak_loc_avg - \
                                    target.peak_tg_pk_before_rel
    target.snr = ((target.peak_tg_pk_rel))/std_dev_labview

    return target

def get_all_target_info(stream, start, std_dev_labview):
    all_target = {}
    all_target['target1'] = get_target_info(stream, start, std_dev_labview)
    all_target['target2'] = get_target_info(stream, start+7, std_dev_labview)
    all_target['target3'] = get_target_info(stream, start+14, std_dev_labview)
    all_target['target4'] = get_target_info(stream, start+21, std_dev_labview)
    all_target['target5'] = get_target_info(stream, start+28, std_dev_labview)

    return all_target

#return the hexadecimal string representation of integer number
def dec2hex(number):
    return "%X" % number

#return the integer value of a hexadecimal string s
def hex2dec(hex_array):
    return int(hex_array.tostring(), 16)

# microcontroller message to display 5 targets
class UcMsg(object):
    def __init__(self):
        self.distance_uc = [0]*5
        self.snr_uc = [0]*5
    def get_info(self, str_uc = ''):
        #delete all the comments insert by Matlab starting with '%'
        foo = str_uc.split('%')[-1]
        list_val = re.findall('\s[0-9]*\.?[0-9]+', foo)
        size = len(list_val)
        item = 0
        while (item < size ):
            self.distance_uc[item//2] = list_val[item]
            self.snr_uc[item//2] = list_val[item + 1]
            item = item + 2

class Histogram(object):
    def __init__(self):
        self.avg = 0
        self.std_dev = 0
        self.std_dev_labview = 0
        self.std_dev_16 = 0
        self.histo_size = 0
        self.raw_data = []

class DistanceOffset(object):
    def __init__(self):
        self.high_power = 0
        self.low_power = 0
        self.low_apd = 0
        self.decr_dist_fact = 0

class Apd(object):
    def __init__(self):
        self.vapd_decr = 0
        self.noise_apd_size = 0
        self.opt_apd_voltage = 0
        self.status_word = 0
        self.noise_distribution = []

class TargetInfo(object):
    def __init__(self):
        self.peak_dist_unit = 0
        self.peak_pos_off3580 = 0
        self.peak_loc_avg = 0
        self.peak_tg_pk_after_rel = 0
        self.peak_tg_pk_after_abs = 0
        self.peak_tg_pk_rel = 0
        self.peak_tg_pk_abs = 0
        self.peak_tg_pk_before_rel = 0
        self.peak_tg_pk_before_abs = 0
        self.snr = 0


#generate the reports after file processing
def do_header_report_mx():

    header = []
    header.append("filename")
    header.append("targetname")
    header.append("target1DIST_uc")
    header.append("target1SNR_uc")
    header.append("target2DIST_uc")
    header.append("target2SNR_uc")
    header.append("shots_nr")
    header.append("Apd.status_word")

    header.append("peak_pos_off3580")
    header.append("peak_tg_pk_rel")
    header.append("peak_loc_avg")
    header.append("peak_tg_pk_abs")
    header.append("snr")
    
    header.append("np_peak_loc_avg")
    header.append("np_peak_tg_pk_abs")
    header.append("np_peak_pos_off3580")
    header.append("np_peak_tg_pk_rel")

    header.append("pkpar3p1d")
    header.append("pkpar3p2d")
    header.append("pkpar3p3d")
    header.append("pkgauss1d")
    header.append("pkpar3pFWHM")
    
    header.append("std_dev_labview")
    header.append("Apd.opt_apd_voltage")

    return header


#generate the reports after file processing
def do_report_mx(filename, mx_cmd_info, target_pos = None, blind_time = 0, frame_len= 100, local_avg_sample= 100):
    print "Generating report for %s" % filename
    if target_pos is None:
        targetname = 'target1'
    else:
        #targetname = choose_target_number(mx_cmd_info, target_pos, blind_time)
        targetname = choose_higherSNRtarget(mx_cmd_info, target_pos, blind_time, frame_len)

    meas_list = []
    meas_list.append(filename)
    meas_list.append(targetname)
    meas_list.append(mx_cmd_info.UcMsg.distance_uc[0])
    meas_list.append(mx_cmd_info.UcMsg.snr_uc[0])
    meas_list.append(mx_cmd_info.UcMsg.distance_uc[1])
    meas_list.append(mx_cmd_info.UcMsg.snr_uc[1])
    meas_list.append(mx_cmd_info.shots_nr)
    meas_list.append(mx_cmd_info.Apd.status_word)
    
    if targetname != None:
        meas_list.append(mx_cmd_info.AllTargetInfo[targetname].peak_pos_off3580)
        meas_list.append(mx_cmd_info.AllTargetInfo[targetname].peak_tg_pk_rel)
        meas_list.append(mx_cmd_info.AllTargetInfo[targetname].peak_loc_avg)
        meas_list.append(mx_cmd_info.AllTargetInfo[targetname].peak_tg_pk_abs)
        meas_list.append(mx_cmd_info.AllTargetInfo[targetname].snr)
    else:
        meas_list=meas_list+[0, 0, 0, 0, 0]
        
    pkpar3p1d, pkpar3p2d, pkpar3p3d, pkgauss1d, pkpar3pFWHM = pf.peak_fit(mx_cmd_info.Histogram.raw_data, target_pos, blind_time, frame_len, local_avg_sample)  
    
    #extract a frame of signal between xmin, xmax    
    xmin = target_pos-frame_len
    xmax = target_pos+frame_len
    if xmin < blind_time:
        xmin = blind_time
    if xmax > len(mx_cmd_info.Histogram.raw_data):
        xmax = len(mx_cmd_info.Histogram.raw_data)
    
    np_peak_loc_avg = np.mean(mx_cmd_info.Histogram.raw_data[target_pos-local_avg_sample:target_pos-10])
    np_peak_tg_pk_abs = np.min(mx_cmd_info.Histogram.raw_data[xmin:xmax])
    np_peak_pos_off3580 = np.argmin(mx_cmd_info.Histogram.raw_data[xmin:xmax])+xmin+1
    np_peak_tg_pk_rel = np_peak_loc_avg - np_peak_tg_pk_abs
    
    meas_list.append(np_peak_loc_avg)
    meas_list.append(np_peak_tg_pk_abs)
    meas_list.append(np_peak_pos_off3580)
    meas_list.append(np_peak_tg_pk_rel)
    meas_list.append(pkpar3p1d)
    meas_list.append(pkpar3p2d)
    meas_list.append(pkpar3p3d)
    meas_list.append(pkgauss1d)
    meas_list.append(pkpar3pFWHM)
    
    meas_list.append(mx_cmd_info.Histogram.std_dev_labview)
    meas_list.append(mx_cmd_info.Apd.opt_apd_voltage)

    return meas_list

def walktree (top = ".", depthfirst = True):
    names = os.listdir(top)
    if not depthfirst:
        yield top, names
    for name in names:
        try:
            os_stat = os.lstat(os.path.join(top, name))
        except os.error:
            continue
        if stat.S_ISDIR(os_stat.st_mode):
            for (newtop, children) in walktree (os.path.join(top, name), \
            depthfirst):
                yield newtop, children
    if depthfirst:
        yield top, names

def extract_comment(file_ptr):
    file_ptr.seek(0)

    try:
        comment_info = file_ptr.readlines()[2]
    except IndexError:
        return []

    #search char '%' into array
    if comment_info[0] is '%':
        try:
            num_regex = re.compile('user: (\w+)')
            user = num_regex.search(comment_info).group(1)
            comment_list = []
            comment_list.append(user)
        except AttributeError:
            comment_list = []

    return comment_list

def main():
    target_distance = 200
    blind_time = 32
    
    #get name of current directory
    base_name = os.path.realpath('./').split('\\')[-1]
    try:
        os.remove('./folder_summary10.txt')
    except WindowsError:
        pass
    fid_wr = open('./folder_summary10.txt', 'a')
    fid_wr.write("%s\n" % base_name)
    header_measure = do_header_report_mx()
    for item in header_measure:
        fid_wr.write("%s, " % item)
    fid_wr.write("\n")
    plt.figure(figsize=(8, 6))
    
    for (basepath, children_filenames) in walktree("./", False):
        for child_filename in children_filenames:
            if child_filename.startswith('Mx'):
                read_filename = os.path.join(basepath, child_filename)
                #read_filename = './Mxtest.txt'
                fid_rd = open(read_filename,'r')

                stream = np.fromfile(file=fid_rd, dtype=np.uint8)

                comment_list = extract_comment(fid_rd)
                fid_rd.close()
                mx_cmd_info = MxCommand()
                mx_cmd_info.load_data_from_mxfile(stream)

                measure_list = do_report_mx(read_filename, mx_cmd_info, target_distance, blind_time)

                # Creates the plot.  No need to save the current figure.
                plt.plot(mx_cmd_info.Histogram.raw_data, label=read_filename)
                num_regex = re.compile('([0-9]*\.?[0-9]+)')
                read_filenumber = num_regex.search(read_filename).group(1)
                mx_cmd_info.Histogram.raw_data.insert(0, int(read_filenumber))

                for item in comment_list:
                    measure_list.append(item)

                for item in measure_list:
                    fid_wr.write("%s, " % item)
                fid_wr.write("\n")

                xmin = target_distance-200
                xmax = target_distance+200

                if xmin < 1 :
                    xmin = 1
                if xmax > len(mx_cmd_info.Histogram.raw_data):
                    xmax = len(mx_cmd_info.Histogram.raw_data)

                ymin = min(mx_cmd_info.Histogram.raw_data[xmin: xmax])*.995
                ymax = max(mx_cmd_info.Histogram.raw_data[xmin: xmax])*1.005
                plt.xlim(xmin, xmax)
                plt.ylim(ymin, ymax)

    fid_wr.close()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()