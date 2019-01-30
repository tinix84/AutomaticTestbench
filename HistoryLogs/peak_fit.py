# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 10:54:06 2012

@author: tricc
"""
import numpy as np
#from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
import sys, re
sys.path.append('../lib/')
from crossing import *


def parabolic_fit_3pt(time, waveform, min_index, frame_idx0, sample_distance = 1):
    """
    Calculate the parabola fitting out of the 3 amplitudes y0 / y1 / y2
    at sampling positions i-1 / i / i+1 where i = position of the peak
    """
    time_fit = [0]*3
    data_to_fit = [0]*3

    dt = time[1]-time[0]
    data_to_fit[1] = np.float32(waveform[min_index])
    time_fit[1] = time[min_index]
    data_to_fit[0] = np.float32(waveform[min_index-sample_distance])
    time_fit[0] = time[min_index-sample_distance]
    data_to_fit[2] = np.float32(waveform[min_index+sample_distance])
    time_fit[2] = time[min_index+sample_distance]
    coeff_par = np.polyfit(time_fit, data_to_fit, 2)

    fit_time = np.linspace(-10*dt, 10*dt, 100) + time[min_index]
    fit_par = np.polyval(coeff_par, fit_time)
    # hold on  plot([0 1 2], data_to_fit)  plot(newtime, ypar, 'r')  hold off
    # calculate the horizontal position of max for a general parabola
    # place into point [0, 1, 2] -> tmax = -b/2a on x = [0, 1, 2]
    tmax_rel = -coeff_par[1]/2/coeff_par[0]
#    # use the displacement calculate before to correct the position
#    # obtained by the max sample
    tmax_abs = frame_idx0+tmax_rel

    return tmax_abs, fit_time, fit_par 

def parabolic_fit_5pt(time, waveform, min_index, frame_idx0, sample_distance = 1):
    """
    Calculate the parabola fitting with LMS out of the 5pt y0/y1/y2/y3/y4
    at sampling positions i-2/i-1/i/i+1/i+2 where i = position of the peak
    """
    time_fit = [0]*5
    data_to_fit = [0]*5

    dt = time[1]-time[0]
    data_to_fit[0] = np.float32(waveform[min_index-2*sample_distance])
    time_fit[0] = time[min_index-2*sample_distance]
    data_to_fit[1] = np.float32(waveform[min_index-sample_distance])
    time_fit[1] = time[min_index-sample_distance]
    data_to_fit[2] = np.float32(waveform[min_index])
    time_fit[2] = time[min_index]
    data_to_fit[3] = np.float32(waveform[min_index+sample_distance])
    time_fit[3] = time[min_index+sample_distance]
    data_to_fit[4] = np.float32(waveform[min_index+2*sample_distance])
    time_fit[4] = time[min_index+2*sample_distance]
    coeff_par = np.polyfit(time_fit, data_to_fit, 2)

    # newtime = np.linspace(0, 2, 100)
    # ypar = np.polyval(coeff_par, newtime)
    # hold on  plot([0 1 2], data_to_fit)  plot(newtime, ypar, 'r')  hold off
    # calculate the horizontal position of max for a general parabola
    # place into point [0, 1, 2] -> tmax = -b/2a on x = [0, 1, 2]
    tmax_rel = -coeff_par[1]/2/coeff_par[0]
    # use the displacement calculate before to correct the position
    # obtained by the max sample
    tmax_abs = frame_idx0+tmax_rel

    return tmax_abs, fit_time, fit_par 

def gaussian_fit_3pt(time, waveform, min_index, frame_idx0, sample_distance = 1):
    """
    Calcs parameters of a peak  gaussian fitting
    The real time position b of the real maximum of the gaussian peak is calculated
    out of the 3 amplitudes y0 / y1 / y2 at sampling positions i-1 / i / i+1
    with i = position of the maximum in histogram with the formulas:
    k = ln (y0/y1) / ln (y2/y1)
    with dx = 30ns for 100MHz/3 corresponding to 4.5m basic resolution
    b = dx {i + (1-k) / (2k+2)}
    """
    time_fit = [0]*3
    data_to_fit = [0]*3

    dt = time[1]-time[0]
    data_to_fit[1] = np.float32(waveform[min_index])
    time_fit[1] = time[min_index]
    data_to_fit[0] = np.float32(waveform[min_index-sample_distance])
    time_fit[0] = time[min_index-sample_distance]
    data_to_fit[2] = np.float32(waveform[min_index+sample_distance])
    time_fit[2] = time[min_index+sample_distance]

    k = np.log(data_to_fit[0]/data_to_fit[1]) / np.log(data_to_fit[2]/data_to_fit[1])
    corr = -(dt*(1-k)/(2*k+2))
    pk = corr+time_fit[1]+frame_idx0
    return pk

def pulse_analisys(histo_data, frame_data, frame_min, frame_min_idx, frame_idx0):
    #interpolation based on Full width at half maximum (FWHM)      
    #calculation od pulse parameters
    low_ref = frame_min #min value for pulse
    #local average of last 100 samples till 10 samples before peak
    high_ref = np.mean(histo_data[frame_min_idx+frame_idx0-100:frame_min_idx+frame_idx0-10])
    mid_ref = (high_ref + low_ref)/2 #half amplitude
    #this calculate the crossing time with a linear approximantion beetween 2 samples points
    idxvect, timevect = crossings(np.arange(frame_data.size), frame_data, mid_ref) 
    #find the two points surrounding the min point, the triplette t0,t1,t2 will be used to approximate
    ind0 = np.nonzero((idxvect[:-1]< frame_min_idx) & (idxvect[1:] > frame_min_idx))[0]
    x0=idxvect[ind0][0]+frame_idx0
    x1=frame_min_idx+frame_idx0
    x2=idxvect[ind0+1][0]+frame_idx0 
    
    pulse_width = timevect[1]-timevect[0]
    
    print timevect
    #print [histo_data[t0], histo_data[t1], histo_data[t2]]
    
    pkpar3pFWHM, time3pFWHM, par3pFWHM = parabolic_fit_3pt([x0,x1,x2],[histo_data[x0], histo_data[x1], histo_data[x2]],1,1)
    #print pkpar3pFWHM
    return pkpar3pFWHM, high_ref, low_ref, mid_ref, pulse_width
    
def peak_fit (histo_data, target_distance, blind_time=100, frame_len=100, local_avg_sample=100):
    #extract a frame of signal between xmin, xmax    
    xmin = target_distance-frame_len
    xmax = target_distance+frame_len
    if xmin < blind_time:
        xmin = blind_time
    if xmax > len(histo_data):
        xmax = len(histo_data)

    frame_data =  np.array(histo_data[xmin: xmax])
    frame_min, frame_min_idx  = frame_data.min(0), frame_data.argmin(0)
    frame_max, frame_max_idx  = frame_data.max(0), frame_data.argmax(0)
    
    pkpar3p1d, time3p1d, par3p1d = parabolic_fit_3pt(np.arange(frame_data.size),frame_data,frame_min_idx, xmin, 1)
    pkpar3p2d, time3p2d, par3p2d = parabolic_fit_3pt(np.arange(frame_data.size),frame_data,frame_min_idx, xmin, 2)
    pkpar3p3d, time3p3d, par3p3d = parabolic_fit_3pt(np.arange(frame_data.size),frame_data,frame_min_idx, xmin, 3)
    pkgauss1d = gaussian_fit_3pt(np.arange(frame_data.size),frame_data,frame_min_idx, xmin, 1)
    pkgauss2d = gaussian_fit_3pt(np.arange(frame_data.size),frame_data,frame_min_idx, xmin, 2)
    pkgauss3d = gaussian_fit_3pt(np.arange(frame_data.size),frame_data,frame_min_idx, xmin, 3)
    
    pkpar3pFWHM, high_ref, low_ref, mid_ref, pulse_width = pulse_analisys(histo_data, frame_data, frame_min, frame_min_idx, xmin)
    
    #print pkpar3p1d, pkpar3p2d, pkpar3p3d
    #print pkgauss1d+xmin, pkgauss2d+xmin, pkgauss3d+xmin
    
    return pkpar3p1d, pkpar3p2d, pkpar3p3d, pkgauss1d, pkpar3pFWHM, pulse_width
    
if __name__ == "__main__":
    
    from lrf_histogram import *
        
    target_distance = 200 #approximate distance of the target express in samples
    blind_time = 32 #beginning blind time to avoid target recognition due to cross coupling
    frame_len= 100 #length of a subset signal around the target
    local_avg_sample=100
    
    read_filename = 'Mx130522150425.txt'
    fid_rd = open(read_filename,'r')
    foo = fid_rd.read()
    stream = re.findall(r'[a-zA-Z0-9_\-\n\r<%\*]', foo)
    fid_rd.close()
    
    mx_cmd_info = MxCommand()
    mx_cmd_info = load_data_from_mxstream(mx_cmd_info, stream)
    
    hist_float32=np.float32(mx_cmd_info['Histogram']['raw_data'])
    pkpar3p1d, pkpar3p2d, pkpar3p3d, pkgauss1d, pkpar3pFWHM, pulse_width = peak_fit(hist_float32, target_distance, blind_time, frame_len, local_avg_sample)  

    print pulse_width
#    # Creates the plot.  No need to save the current figure.
#    plt.plot(mx_cmd_info['Histogram']['raw_data'])
#    plt.xlim(xmin, xmax)
#    plt.ylim(ymin*.995, ymax*1.005)
#    
#    plt.plot(ydata)
#    plt.ylim(ymin*.995, ymax*1.005)
#    plt.plot(time3p1d+xmin, par3p1d)
#    plt.plot(time3p2d+xmin, par3p2d)
#    plt.plot(time3p3d+xmin, par3p3d)
#    plt.plot(np.arange(ydata.size)+xmin,high_ref*np.ones(np.size(ydata)))   
#    plt.plot(np.arange(ydata.size)+xmin,low_ref*np.ones(np.size(ydata)))  
#    plt.plot(np.arange(ydata.size)+xmin,mid_ref*np.ones(np.size(ydata)))  
#    plt.show()