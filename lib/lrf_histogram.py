## @package pyexample
#  Documentation for this module.
#
#  More details.

# {{{ http://code.activestate.com/recipes/534109/ (r8)


from __future__ import division
import os
import stat
import re
import numpy as np

import sys
sys.path.append('../include/')
from cmdmx_constant import *

## Documentation for a class.
#
#  More details.
def MxCommand():
	mxCmdInfo={}
	mxCmdInfo['lrf_raw_stream'] = ''
	mxCmdInfo['UcMsg'] = UcMsg()
	# Create an empty Histogram record
	mxCmdInfo['Histogram'] = Histogram()
	# Create an empty offset setting record
	mxCmdInfo['DistanceOffset'] = DistanceOffset()
	mxCmdInfo['target'] = {}
	mxCmdInfo['target']['t1'] = TargetInfo()
	mxCmdInfo['target']['t2'] = TargetInfo()
	mxCmdInfo['target']['t3'] = TargetInfo()
	mxCmdInfo['target']['t4'] = TargetInfo()
	mxCmdInfo['target']['t5'] = TargetInfo()

	# Create an empty Apd record
	mxCmdInfo['Apd'] = Apd()
	mxCmdInfo['shots_nr'] = 0
	mxCmdInfo['swVersion'] = None
	mxCmdInfo['validTarget'] = 0
	
	return mxCmdInfo

## Documentation for a function.
#
#  choose the target based to the distance from a given target.
def choose_target_number(mxCmdInfo, target_pos, min_distance=8000 ):
    for item in mxCmdInfo['target'].keys() :
        distance = abs(target_pos - mxCmdInfo['target'][item]['peak_pos_off3580'])
        if min_distance > distance :
            min_distance = distance
            closer_target = item
    return closer_target

## Documentation for a function.
#
#  def get_dec_param(stream = [], start= 0, stop = start):
def get_dec_param(*arg):
    stream = arg[0]
    start = arg[1]
    if len(arg) < 3:
        stop = start #if not defined stop=start
    else:
        stop = arg[2]
    # Multiplication by 6 is due to the 24bits are trasmitter as a char
    par = stream[6*start-6:6*stop]

    return par

## Documentation for a function.
#
#  def get_hex_param(stream = [], start= 0, stop = start):
def get_hex_param(*arg):
    stream = arg[0]
    start = arg[1]
    if len(arg) < 3:
        stop = start
    else:
        stop = arg[2]
    # Multiplication by 6 is due to the 24bits are trasmitter as a char
    par = hex2dec(stream[6*start-6:6*stop])

    return par

## Documentation for a function.
#
#  More details.
def get_histogram_data(stream, start, stop):
    histo = get_dec_param(stream, start, stop)
    histo_dec = []
    for item in range(0, len(histo), 6):
        histo_dec.append(hex2dec(histo[item:item+6]))

    return histo_dec

## Documentation for a function.
#
#  More details.
def get_apd_noise_distribution(stream, start, stop):
    apd_distr = get_dec_param(stream, start, stop)
    apd_distr_dec = []
    for item in range(0, len(apd_distr), 6):
        apd_distr_dec.append(hex2dec(apd_distr[item:item+6]))

    return apd_distr_dec

## Documentation for a function.
#
#  More details.
def get_target_info(stream, start, std_dev_labview):
    target = {}
    target['peak_dist_unit'] = ''.join(get_dec_param(stream, start))
    target['peak_pos_off3580'] = get_hex_param(stream, start+1)-3580
    target['peak_loc_avg'] = get_hex_param(stream, start+2)
    target['peak_tg_pk_after_rel'] = get_hex_param(stream, start+3)
    target['peak_tg_pk_after_abs'] = target['peak_loc_avg'] - target['peak_tg_pk_after_rel']
    target['peak_tg_pk_rel'] = get_hex_param(stream, start+4)
    target['peak_tg_pk_abs'] = target['peak_loc_avg']-target['peak_tg_pk_rel']
    target['peak_tg_pk_before_rel'] = get_hex_param(stream, start+5)
    target['peak_tg_pk_before_abs'] = target['peak_loc_avg'] - target['peak_tg_pk_before_rel']
    target['snr'] = target['peak_tg_pk_rel']/std_dev_labview
    return target

## Documentation for a function.
#
#  More details.
def get_all_target_info(stream, start, std_dev_labview):
    all_target = {}
    all_target['t1'] = get_target_info(stream, start, std_dev_labview)
    all_target['t2'] = get_target_info(stream, start+7, std_dev_labview)
    all_target['t3'] = get_target_info(stream, start+14, std_dev_labview)
    all_target['t4'] = get_target_info(stream, start+21, std_dev_labview)
    all_target['t5'] = get_target_info(stream, start+28, std_dev_labview)
    return all_target

## Documentation for a function.
#
#  return the hexadecimal string representation of integer number
def dec2hex(number):
    return "%X" % number

## Documentation for a function.
#
#  return the integer value of a hexadecimal string s
def hex2dec(hex_array):
    return int(''.join(hex_array), 16)

## Documentation for a function.
#
#  microcontroller message to display 5 targets 
def UcMsg():
    uCmsg={}
    uCmsg['distance_uc'] = [0]*5
    uCmsg['snr_uc'] = [0]*5  
    return uCmsg

def get_info_uc(uCmsg, str_uc = ''):
    #delete all the comments insert by Matlab starting with '%'
    foo = str_uc.split('%')[-1]
    print foo
    list_val = re.findall('\s[0-9]*\.?[0-9]+', foo)
    print list_val
    size = len(list_val)
    print size
    item = 0
    while (item < size ):
        uCmsg['distance_uc'][item//2] = list_val[item]
        uCmsg['snr_uc'][item//2] = list_val[item + 1]
        item = item + 2
    return uCmsg
    
## Documentation for a class.
#
#  More details.
def Histogram():
	hist={}
	hist['avg'] = 0
	hist['std_dev'] = 0
	hist['std_dev_labview'] = 0
	hist['std_dev_16'] = 0
	hist['histo_size'] = 0
	hist['raw_data'] = []
	return hist

## Documentation for a class.
#
#  More details.
def DistanceOffset():
	dist={}
	dist['high_power'] = 0
	dist['low_power'] = 0
	dist['low_apd'] = 0
	dist['decr_dist_fact'] = 0
	
	return dist

## Documentation for a class.
#
#  More details.
def Apd():
	apd={}
	apd['vapd_decr'] = 0
	apd['noise_apd_size'] = 0
	apd['opt_apd_voltage'] = 0
	apd['status_word'] = 0
	apd['noise_distribution'] = []
	
	return apd 

## Documentation for a class.
#
#  More details.
def TargetInfo():
	target={}
	target['peak_dist_unit'] = 0
	target['peak_pos_off3580'] = 0
	target['peak_loc_avg'] = 0
	target['peak_tg_pk_after_rel'] = 0
	target['peak_tg_pk_after_abs'] = 0
	target['peak_tg_pk_rel'] = 0
	target['peak_tg_pk_abs'] = 0
	target['peak_tg_pk_before_rel'] = 0
	target['peak_tg_pk_before_abs'] = 0
	target['snr'] = 0
	
	return target

## Documentation for a function.
#
#  generate the reports after file processing
def do_report_mx(filename, mxCmdInfo, target_pos = None):
    if target_pos is None:
        targetname = 't1'
    else:
        targetname = choose_target_number(mxCmdInfo, target_pos)

    meas_list = []
    meas_list.append(filename)
    meas_list.append(targetname)
    meas_list.append(mxCmdInfo['UcMsg']['distance_uc'][0])
    meas_list.append(mxCmdInfo['UcMsg']['snr_uc'][0])
    meas_list.append(mxCmdInfo['shots_nr'])
    meas_list.append(mxCmdInfo['Apd']['status_word'])

    meas_list.append(mxCmdInfo['target'][targetname]['peak_pos_off3580'])
    meas_list.append(mxCmdInfo['target'][targetname]['peak_tg_pk_rel'])
    meas_list.append(mxCmdInfo['target'][targetname]['peak_loc_avg'])
    meas_list.append(mxCmdInfo['target'][targetname]['peak_tg_pk_abs'])
    meas_list.append(mxCmdInfo['target'][targetname]['snr'])

    np_peak_loc_avg = np.mean(mxCmdInfo['Histogram']['raw_data'][0:7])
    np_peak_tg_pk_abs = np.min(mxCmdInfo['Histogram']['raw_data'])
    np_peak_pos_off3580 = np.argmin(mxCmdInfo['Histogram']['raw_data'])
    np_peak_tg_pk_rel = np_peak_loc_avg - np_peak_tg_pk_abs
    meas_list.append(np_peak_pos_off3580)
    meas_list.append(np_peak_tg_pk_rel)
    meas_list.append(np_peak_loc_avg)
    meas_list.append(np_peak_tg_pk_abs)
    meas_list.append(mxCmdInfo['Histogram']['std_dev_labview'])

    meas_list.append(mxCmdInfo['Apd']['opt_apd_voltage'])

    return meas_list

## Documentation for a function.
#
#  More details.
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

## Documentation for a function.
#
#  More details.
def extract_comment(file_ptr):
    file_ptr.seek(0)
    file_ptr.seek(0)
    try:
        comment_info = file_ptr.readlines()[1]
    except IndexError:
        return []

    #search char '%' into array
    if comment_info[0] is '%':
        try:
            num_regex = re.compile('(\w+)_Att')
            mb_sw = num_regex.search(comment_info).group(1)
            num_regex = re.compile('_Att([0-9]*\.?[0-9]+)_')
            opt_att_dB = num_regex.search(comment_info).group(1)
            num_regex = re.compile('_APD([0-9]*\.?[0-9]+)')
            voltage_apd_V = num_regex.search(comment_info).group(1)
            num_regex = re.compile('_stdRX([0-9]*\.?[0-9]+)')
            stdnoise_rx_mV = num_regex.search(comment_info).group(1)
            num_regex = re.compile('_stdMB([0-9]*\.?[0-9]+)')
            stdnoise_adc_mV = num_regex.search(comment_info).group(1)
            num_regex = re.compile('_Rf([0-9]*\.?[0-9]+)')
            rf_rx_kohm = num_regex.search(comment_info).group(1)
            comment_list = []
            comment_list.append(mb_sw)
            comment_list.append(opt_att_dB)
            comment_list.append(voltage_apd_V)
            comment_list.append(stdnoise_rx_mV)
            comment_list.append(stdnoise_adc_mV)
            comment_list.append(rf_rx_kohm)
        except AttributeError:
            comment_list = []
    else:
        comment_list = []

    return comment_list

## Documentation for a method.
#  @param mxobj The object pointer.
def load_data_from_mxstream (mxobj, stream_char= ""):
    try:
    #search char '*' into array
        uc_msg_len = stream_char.index('*')
        histo_str = stream_char[uc_msg_len+2:]
        str_uc = ''.join(stream_char[0:uc_msg_len+2])
        mxobj['UcMsg']=get_info_uc(mxobj['UcMsg'], str_uc)
    except ValueError:
        histo_str = stream_char
    
    mxobj['lrf_raw_stream'] = stream_char
    # Multiplication by 6 is due to the 24bits are trasmitter as a nibble
    # HistogramSize
    mxobj['Histogram']['avg'] = get_hex_param(histo_str, WORD_NR_AVG_HISTO)
    mxobj['Histogram']['std_dev'] = get_hex_param(histo_str, WORD_NR_STD_DEV)
    mxobj['Histogram']['std_dev_labview'] = mxobj['Histogram']['std_dev']/4
    mxobj['Histogram']['std_dev_16'] = mxobj['Histogram']['std_dev_labview']/16
    
    # HistogramSize
    mxobj['Apd']['vapd_decr'] = get_hex_param(histo_str, WORD_NR_VAPD_DECR)
    mxobj['shots_nr'] = get_hex_param(histo_str, WORD_NR_SHOTS_NR)
    # LRFOffset
    mxobj['DistanceOffset']['high_power'] = get_hex_param(histo_str, WORD_NR_HP_DIST_OFFSET)
    mxobj['DistanceOffset']['low_power'] = get_hex_param(histo_str, WORD_NR_LP_DIST_OFFSET)
    mxobj['DistanceOffset']['low_apd'] = get_hex_param(histo_str, WORD_NR_LAPD_DIST_OFFSET)
    mxobj['DistanceOffset']['decr_dist_fact'] = get_hex_param(histo_str, WORD_NR_DECR_DIST_FACT)
    
    # Histogram Size
    mxobj['Histogram']['histo_size'] = get_hex_param(histo_str, WORD_NR_HISTO_SIZE)
    histo_len = mxobj['Histogram']['histo_size']
    # noise_distribution Size
    mxobj['Apd']['noise_apd_size'] = get_hex_param(histo_str, WORD_NR_NOISE_DISTR)
    apd_distr_len = mxobj['Apd']['noise_apd_size']
    # variable definition after having read apd_distr_len and histo_len
    word_nr_status_word = 65+apd_distr_len
    word_nr_opt_apd_voltage = 66+apd_distr_len
    word_nr_apd_distr = range(65,80,1)
    word_nr_histo = range(67+apd_distr_len,66+apd_distr_len+histo_len,1)
    word_nr_peak1_dist_decunit = 68+apd_distr_len+histo_len
    word_nr_valid_peaks = 102+apd_distr_len+histo_len
    word_nr_sw_ver = 103+apd_distr_len+histo_len
    
    mxobj['Apd']['opt_apd_voltage'] = get_hex_param(histo_str,word_nr_opt_apd_voltage)
    mxobj['Apd']['status_word'] = ''.join(get_dec_param(histo_str, word_nr_status_word))
    mxobj['Apd']['noise_distribution'] = get_apd_noise_distribution(histo_str, word_nr_apd_distr[1], word_nr_apd_distr[-1])
    mxobj['Histogram']['raw_data'] = get_histogram_data(histo_str, word_nr_histo[0], word_nr_histo[-1])
    
    mxobj['valid_target'] = get_hex_param(histo_str, word_nr_valid_peaks)
    mxobj['swVersion'] = str(get_dec_param(histo_str, word_nr_sw_ver))
    mxobj['target'] = get_all_target_info(histo_str, word_nr_peak1_dist_decunit, mxobj['Histogram']['std_dev_labview'])
    
    return mxobj
		  
### Documentation for a function.
##
##  More details.
#def main():
#    target_distance = 7000
#    #get name of current directory
#    base_name = os.path.realpath('./').split('\\')[-1]
#    try:
#        os.remove('./folder_summary.txt')
#    except WindowsError:
#        pass
#    fid_wr = open('./folder_summary.txt', 'a')
#    fid_wr.write("%s\n" % base_name)
#    plt.figure(figsize=(8, 6))
#    fid_csvrawdata = open('./rawdata_summary.csv', 'wt')
#    csvwriter = csv.writer(fid_csvrawdata, dialect = csv.excel)
#
#    for (basepath, children_filenames) in walktree("./", False):
#        for child_filename in children_filenames:
#            if child_filename.startswith('Mx'):
#                read_filename = os.path.join(basepath, child_filename)
#                read_filename = '../Mx120508193220.txt'
#                fid_rd = open(read_filename,'r')
##                file_info = fid_rd.readlines()
#                foo = fid_rd.read()
#                stream = re.findall(r'[a-zA-Z0-9_\-\n\r<%\*]', foo)
##                stream = stream[1:-1].split(',')
##                stream = np.fromfile(file=fid_rd, dtype=np.uint8)
#                #stream = array.array("B")  # L is the typecode for uint32
##                try:
##                    stream.fromfile(fid_rd, 65536)
##                except EOFError:
##                    pass
#                ## start from the beginning
##                fid_rd.seek(0)
##                fid_rd.seek(0)
##                lab_info = fid_rd.readlines()[1]
##                vAPD_V = re.findall('[0-9]*\.?[0-9]+', lab_info)[0]
##                stdNoise_mV = re.findall('[0-9]*\.?[0-9]+', lab_info)[1]
#
#                comment_list = extract_comment(fid_rd)
#                fid_rd.close()
#                mxCmdInfo = MxCommand()
#                mxCmdInfo = load_data_from_mxstream(mxCmdInfo, stream)
#  
#                measure_list = do_report_mx(read_filename, mxCmdInfo, target_distance)
#                # Creates the plot.  No need to save the current figure.
#                plt.plot(mxCmdInfo['Histogram']['raw_data'])
#                num_regex = re.compile('m([0-9]*\.?[0-9]+)')
##                read_filenumber = num_regex.search(read_filename).group(1)
##                mxCmdInfo.Histogram.raw_data.insert(0, int(read_filenumber))
##                csvwriter.writerow(['mxCmdInfo']['Histogram']['raw_data'])
#
#                for item in comment_list:
#                    measure_list.append(item)
#
#                for item in measure_list:
#                    fid_wr.write("%s, " % item)
#                fid_wr.write("\n")
#
##                xmin = target_distance-50
##                xmax = target_distance+50
##
##                if xmin < 100 :
##                    xmin = 100
##                if xmax > len(mxCmdInfo.Histogram.raw_data):
##                    xmax = len(mxCmdInfo.Histogram.raw_data)
##
##                ymin = min(mxCmdInfo.Histogram.raw_data[xmin: xmax])*.995
##                ymax = max(mxCmdInfo.Histogram.raw_data[xmin: xmax])*1.005
##                plt.xlim(xmin, xmax)
##                plt.ylim(ymin, ymax)
##
#    fid_wr.close()
#    fid_csvrawdata.close()
#    plt.show()
#
#if __name__ == "__main__":
#    main()
