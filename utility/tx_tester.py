# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:09:10 2012

@author: tricc
"""
import generic_port
import sys, time, msvcrt

import datetime
import func_gen_drv as fxgen
import oscilloscope_drv as osc
import afg_protocol as afgp
import lecroy_protocol as lcp
import lrf_tx

PRESS_TIMEOUT = 5
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

    time_filename = timeStamped('_')
    log_filename = time_filename+'log.txt'

    sys.stdout = MyLogOutput(log_filename)

    meas_filename = time_filename+'meas.txt'
    print_screen_filename= time_filename+'tx'
    print "  --> log_file: `%s'" % log_filename
    log_file =open(log_filename,'a')
    meas_file =open(meas_filename,'a')
    log_header='Log starts @:'+str(datetime.datetime.now())
    print log_header
    meas_file.write(log_header)
    meas_file.write('\nSupply Voltage, Number of pulses, Induct, AP015 Peak Supply Current,' \
                     'Electrical PWM width, PWM Period, Total Inductor Charge,' \
                     'Electrical TRG pulse width, TRG Period, Nominal Caps,' \
                     'MeasCaps voltages, Peak Laser Current Probe, Current probe pulse width,' \
                     'Current pulse area, PIN optical pulse width\n')
    meas_file.close()

    scope_address = '192.168.1.4'
    scope_lan_port = 1861
    scope_protocol = 'TCPIP'
    scope_port = generic_port.ActiveXLeCroyPort(scope_protocol, scope_address, None)
    scope = osc.LeCroyWaveRunner610Zi(scope_port)
    scope.connect()
    print "  --> scope id: `%s'" % scope.identify()
    #scope.recall_setup_from_file('D:\GaNTxPWM112us')
    time.sleep(2)

    gen_address = 4
    gen_port = None
    gen_protocol = 'GPIB'
    gen_port = generic_port.PyVisaPort(gen_protocol, gen_address, gen_port)
    gen = fxgen.AFG3102(gen_port)
    gen.connect()
    #gen.reset()
    print "  --> gen id: `%s'" % gen.identify()

    #Initialization
    dut=lrf_tx.create_enh_tx(lrf_tx.GenericLRFTx())
    #lrf_tx.print_charge_pattern(dut)

    dut.C = 660e-9
    dut.L = 10e-6
    dut.pwm_on=6.8e-6
    dut.pwm_off=2.4e-6
    dut.trg_delay=112e-6
    dut.trg_on=500e-9
    dut.update()

    #gen.recall_setup_from_memory(3)
    time.sleep(1)
    gen.set_pulse_period(1, dut.pwm_period)
    gen.set_pulse_period(2, dut.trg_period)

    gen.set_burst_cycles(1, 1)
    gen.set_burst_cycles(2, 1)
    gen.set_burst_trigger_delay(1, 0)
    gen.set_burst_trigger_delay(2, dut.trg_delay)
    gen.set_pulse_width(1, dut.pwm_on)
    gen.set_pulse_width(2, dut.trg_on)

    gen.set_output_on(1)
    gen.set_output_on(2)

    cycl_max = 12#dut.pwm_cycles_max
    print "\nMAX_PWM_CYCLES:%d\n" % cycl_max

    for cycl in range(1, cycl_max+1):
        meas_list = []
        dbg_list = []

        startTime = time.time()
        print "Press ESC to stop... or wait 2 seconds... "
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
            print "\nPWM_CYCLES:%s" % cycl
            gen.set_burst_cycles(1, cycl)
            gen.trigger()


            pk_current=scope.get_meas_max(lcp.function[1])
            print pk_current

            pulse_width=scope.get_meas_width(lcp.function[1])
            print pulse_width

            pulse_area=scope.get_meas_area(lcp.function[1])
            print pulse_area

            optpulse_width=scope.get_meas_width(lcp.function[2])
            print optpulse_width

            cap_voltage=scope.get_meas_max(lcp.channel[1])
            print cap_voltage

            max_input_current=scope.get_meas_max(lcp.channel[2])
            print max_input_current

            input_charge=scope.get_meas_area(lcp.channel[2])
            print input_charge

            scope.print_screen_tif(print_screen_filename+str(cycl) +'.tif')

            meas_list.append((dut.Vsupply))
            meas_list.append((cycl))
            meas_list.append((dut.L))
            meas_list.append(meas2num(max_input_current))
            meas_list.append((dut.pwm_on))
            meas_list.append((dut.pwm_period))
            meas_list.append(meas2num(input_charge))
            meas_list.append((dut.trg_on))
            meas_list.append((dut.trg_period))
            meas_list.append((dut.C))
            meas_list.append(meas2num(cap_voltage))
            meas_list.append(meas2num(pk_current)*10**1.5)
            meas_list.append(meas2num(pulse_width))
            meas_list.append(meas2num(pulse_area)*10**1.5/1000)
            meas_list.append(meas2num(optpulse_width))

            log_data(meas_filename, meas_list)

    gen.set_output_off(1)
    gen.set_output_off(2)

    scope.disconnect()
    gen.disconnect()
