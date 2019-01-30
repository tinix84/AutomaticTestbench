# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:09:10 2012

@author: tricc
"""
import sys, time, msvcrt
import datetime

sys.path.append('../dev/')
import generic_port
#import func_gen_drv as fxgen
import activeload_drv as load
import powersupply_drv as pwrgen
import multimeter_drv as dmm
#import oscilloscope_drv as osc
#import afg_protocol as afgp
#import lecroy_protocol as lcp
#import lrf_tx


PRESS_TIMEOUT = 3
inp = None

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

def meas2num(meas_str):
    value=meas_str.split(',')[1]
    try:
        out=float(value)
    except ValueError:
        out = '#'
    return out

def timeStamped(fname, fmt='%Y%m%d%H%M%S{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

def get_all_measure():
    pass

def log_data(filename, data_list):
    fp =open(filename,'a')
    fp.writelines(["%s, " % item for item in data_list])
    fp.write("\n")
    fp.close()


if __name__ == "__main__":
    
    directory='../HistoryLogsDCDC/'
    time_filename = directory+timeStamped('_')
    log_filename = directory+time_filename+'log.txt'

    sys.stdout = MyLogOutput(log_filename)
    
    meas_filename = time_filename+'MODULE2_TPS63031PS0LC_Tm40.txt'
    print_screen_filename= time_filename+'MODULE2_TPS63031PS0LC'
    print "  --> log_file: `%s'" % log_filename
    log_file =open(log_filename,'a')
    meas_file =open(meas_filename,'a')
    log_header='Log starts @:'+str(datetime.datetime.now())
    print log_header
    meas_file.write(log_header)
    meas_file.write('\nVin_set, Io_set, Vin, Iin, Vout, Iout, ' \
                     'Pin, Po, Eff, Po_Iset, Eff_Iset\n' )
    meas_file.close()

    load_board = 0
    load_address = 4
    load_protocol = 'GPIB'
    load_port = generic_port.PyVisaPort(load_protocol, load_address, load_board)
    load = load.KikusuiPLZ164W(load_port)
    load.connect()
    print "  --> scope id: `%s'" % load.identify()
    time.sleep(1)

    pwrgen_board = 0
    pwrgen_address = 2
    pwrgen_protocol = 'GPIB'
    pwrgen_port = generic_port.PyVisaPort(pwrgen_protocol, pwrgen_address, pwrgen_board)
    pwrgen = pwrgen.E3631A(pwrgen_port)
    pwrgen.connect()
    print "  --> gen id: `%s'" % pwrgen.identify()
    pwrgen.reset()
    time.sleep(1)
    
    dmmvin_board = 0
    dmmvin_address = 3
    dmmvin_protocol = 'GPIB'
    dmmvin_port = generic_port.PyVisaPort(dmmvin_protocol, dmmvin_address, dmmvin_board)
    vin_dmm = dmm.HP34401A(dmmvin_port)
    vin_dmm.connect()
    print "  --> gen id: `%s'" % vin_dmm.identify()
    vin_dmm.reset()
    time.sleep(1)
    
    dmmiin_board = 0
    dmmiin_address = 22
    dmmiin_protocol = 'GPIB'
    dmmiin_port = generic_port.PyVisaPort(dmmiin_protocol, dmmiin_address, dmmiin_board)
    iin_dmm = dmm.HP34401A(dmmiin_port)
    iin_dmm.connect()
    print "  --> gen id: `%s'" % iin_dmm.identify()
    iin_dmm.reset()
    time.sleep(1)
    
    #Initialization
    vin_min=2.7
    vin_max=5.6 
    vin_step=.1
    
#    vin_vect=[4.5, 5, 5.5]
#    iout_min=1
#    iout_max=2
#    iout_step=.1

    vin_vect=[2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.5, 4, 4.5, 5, 5.5]
#    iout_vect=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
#    temp_vect=[-40, -20, 0, 25, 50, 70, 85]
    
#    vin_vect=[4, 4.5, 5, 5.5]
    iout_vect=[0, 0.025, 0.050, 0.075, 0.100, 0.125, 0.150, 0.175, 0.2]
#    iout_vect=[0, 0.001, 0.002, 0.005, 0.010, 0.015, 0.020, 0.025]
#    iout_vect=[0, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.009, 0.001]
    temp_vect=[-40, -20, 0, 25, 50, 70, 85]
    
    #calculation of expected values
    vout_min=8.25*0.95
    vout_max=8.25*1.05
    #factor 2 is to compensate a drop of 2 of efficiency
#    iin_max=vout_max*iout_max/vin_min*2
    iin_max=.7
    iout_max=iout_vect[-1]*10
    
    load.set_constant_current_mode()
    load.set_current_range_low()

    vin_dmm.set_voltage_mode(vin_max)
    vin_dmm.set_trigger_source_immediate() 
    
    iin_dmm.set_current_mode(1,1e-6)
    iin_dmm.set_trigger_source_immediate() 
 
    for vin in vin_vect:
        startTime = time.time()
        print "Press ESC to stop... or wait 3 seconds... "
        while True:
            if msvcrt.kbhit():
                inp = msvcrt.getch()
                break
            elif time.time() - startTime > PRESS_TIMEOUT:
                break 
        if inp:
            print "ESC pressed, measurement aborted..."
            break
        else:
            pwrgen.set_P6Vchannel_voltage_current(vin, iin_max)
            pwrgen.set_all_output_on()
            time.sleep(1)  
            for iout in iout_vect:
                #print "\nVin=: %s \tIout=%s " % (vin, iout)
                meas_list = []
                dbg_list = [] 

                load.set_current_value(iout)

                load.set_load_on()
                time.sleep(1)
        
                vinLC_meas=float(pwrgen.get_P6Vchannel_measure_voltage())
                vin_meas=float(vin_dmm.get_measure())
                iin_meas=float(iin_dmm.get_measure())
                time.sleep(.5)
                iout_meas=float(load.get_measure_current())
                time.sleep(.5)
                vout_meas=float(load.get_measure_voltage())
        
                #load.set_load_off()    
                time.sleep(1)    

                pwrin=vin_meas*iin_meas
                pwrout=vout_meas*iout_meas  
                eff=pwrout/pwrin
                pwrout_iset=vout_meas*iout  
                eff_iset=pwrout_iset/pwrin                
      
                print "Vset=%.3e, Iset=%.3e, VinLC=%.3e, Vin=%.3e, Iin=%.3e, Vout=%.3e, Iout=%.3e, Pin=%.3e, Pout=%.3e, eff=%.3e" \
                        %  (vin, iout, vinLC_meas, vin_meas, iin_meas, vout_meas, iout_meas, pwrin, pwrout, eff)
               
                meas_list.append(vin)      
                meas_list.append(iout)                
                meas_list.append(vinLC_meas)
                meas_list.append(vin_meas)                
                meas_list.append(iin_meas)
                meas_list.append(vout_meas)
                meas_list.append(iout_meas)
                meas_list.append(pwrin)
                meas_list.append(pwrout)
                meas_list.append(eff)     
                meas_list.append(pwrout_iset)
                meas_list.append(eff_iset) 
                log_data(meas_filename, meas_list)

            pwrgen.set_all_output_off()
            load.set_load_off()  
            
    pwrgen.disconnect() 
    load.disconnect()
    vin_dmm.disconnect()
    iin_dmm.disconnect()
