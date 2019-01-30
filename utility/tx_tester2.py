# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 13:09:10 2012

@author: tricc
"""
import generic_port
import sys, time, msvcrt
import numpy as np
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

#def meas2num(meas_str):
#    value = meas_str.split(',')[1]
#    try:
#        out = float(value)
#    except ValueError:
#        out = '#'
#    return out

def timeStamped(fname, fmt='%Y%m%d%H%M%S{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname = fname)

def get_all_measure():
    pass

def log_data(filename, data_list):
    fp = open(filename,'a')
    fp.writelines(["%s " % item for item in data_list])
    fp.write("\n")
    fp.close()

class LaserEnergyTset():
    def __init__(self):
        #Initialization
        #laser I/V fitting coefficient
        self.laser_fit_coeff = [15.51e-6, 4, 0.0599]

        enhtx_gen = lrf_tx.create_enh_tx(lrf_tx.GenericLRFTx())
        self.tx_dut = lrf_tx.create_custom_tx(enhtx_gen)

        scope_address = '192.168.1.10'
        scope_lan_port = 1861
        scope_protocol = 'TCPIP'
        scope_port = generic_port.ActiveXLeCroyPort(scope_protocol, scope_address, None)

        self.tx_adc_cfg = { 'inductor_current' : 1, 'capacitor_voltage' : 2,
          'pin_voltage' : 3, 'laser_current' : 4, }

        self.tx_adc = osc.LeCroyWaveRunner610Zi(scope_port)
        self.tx_adc.connect()
        print "  --> tx_adc id: `%s'" % self.tx_adc.identify()
        #self.tx_adc.recall_setup_from_file('D:\GaNTxPWM112us')

        gen_address = 4
        gen_port = None
        gen_protocol = 'GPIB'
        gen_port = generic_port.PyVisaPort(gen_protocol, gen_address, gen_port)

        self.tx_drv = fxgen.AFG3102(gen_port)
        self.tx_drv.connect()
        #gen.reset()
        print "  --> self.tx_drv id: `%s'" % self.tx_drv.identify()

        self.tx_drv_cfg = { 'pwm' : 1, 'trg' : 2,}
        self.init_tx_drv()
        self.pwm_burst_cycles = self.tx_dut.pwm_cycles_max

        self.meas_list = []
        self.probe_dBatt = 30
        
        self.log_directory = None
        self.meas_filename = None
        self.log_filename = None
        self.meas_file = None
        self.log_file = None
        self.prtsc_filename = None
       
    def shoot(self):
        self.tx_drv.trigger()

    def set_pwm_output_on(self):
        self.tx_drv.set_output_on(self.tx_drv_cfg['pwm'])

    def set_pwm_output_off(self):
        self.tx_drv.set_output_off(self.tx_drv_cfg['pwm'])

    def set_trg_output_on(self):
        self.tx_drv.set_output_on(self.tx_drv_cfg['trg'])

    def set_trg_output_off(self):
        self.tx_drv.set_output_off(self.tx_drv_cfg['trg'])

    def set_pwm_high(self, value):
        self.tx_drv.set_voltage_high(self.tx_drv_cfg['pwm'], value)

    def set_pwm_low(self, value):
        self.tx_drv.set_voltage_low(self.tx_drv_cfg['pwm'], value)

    def set_pwm_risetime(self, value):
        self.tx_drv.set_pulse_risetime(self.tx_drv_cfg['pwm'], value)

    def set_pwm_falltime(self, value):
        self.tx_drv.set_pulse_falltime(self.tx_drv_cfg['pwm'], value)

    def set_pwm_period(self, value):
        self.tx_drv.set_pulse_period(self.tx_drv_cfg['pwm'], value)

    def set_pwm_width(self, value):
        self.tx_drv.set_pulse_width(self.tx_drv_cfg['pwm'], value)

    def set_pwm_delay(self, value):
        self.tx_drv.set_burst_trigger_delay(self.tx_drv_cfg['pwm'], value)

    def set_pwm_cycle(self, value):
        self.tx_drv.set_burst_cycles(self.tx_drv_cfg['pwm'], value)

    def set_trg_high(self, value):
        self.tx_drv.set_voltage_high(self.tx_drv_cfg['trg'], value)

    def set_trg_low(self, value):
        self.tx_drv.set_voltage_low(self.tx_drv_cfg['trg'], value)

    def set_trg_risetime(self, value):
        self.tx_drv.set_pulse_risetime(self.tx_drv_cfg['trg'], value)

    def set_trg_falltime(self, value):
        self.tx_drv.set_pulse_falltime(self.tx_drv_cfg['trg'], value)

    def set_trg_period(self, value):
        self.tx_drv.set_pulse_period(self.tx_drv_cfg['trg'], value)

    def set_trg_width(self, value):
        self.tx_drv.set_pulse_width(self.tx_drv_cfg['trg'], value)

    def set_trg_delay(self, value):
        self.tx_drv.set_burst_trigger_delay(self.tx_drv_cfg['trg'], value)

    def set_trg_cycle(self, value):
        self.tx_drv.set_burst_cycles(self.tx_drv_cfg['trg'], value)

    def init_tx_adc(self):
        self.tx_adc.recall_setup_from_file('D:\GaNTxPWM112us')
        time.sleep(3)

    def get_peak_inductor_current(self):
        max_input_current = self.tx_adc.get_meas_max(lcp.channel[2])
        return (max_input_current)

    def get_width_laser_current(self):
        pulse_width = self.tx_adc.get_meas_width(lcp.function[1])
        return (pulse_width)

    def get_peak_laser_current(self):
        pk_current = self.tx_adc.get_meas_max(lcp.function[1])
        return (pk_current)*10**(self.probe_dBatt/20)

    def get_area_laser_current(self):
        pulse_area = self.tx_adc.get_meas_area(lcp.function[1])
        return (pulse_area)*10**(self.probe_dBatt/20)/1000

    def get_charge_inductor(self):
        input_charge = self.tx_adc.get_meas_area(lcp.channel[2])
        return (input_charge)

    def get_max_capacitor_voltage(self):
        cap_voltage = self.tx_adc.get_meas_max(lcp.channel[1])
        return (cap_voltage)

    def get_width_laser_PIN(self):
        return '#'

    def get_prtscr(self, cycle):
        self.tx_adc.print_screen_tif(self.prtsc_filename+str(cycle) +'.tif')


    def collect_data(self):
        # calculation of data for csv
        theo_charge_ind = self.tx_dut.pwm_burst_cycles*self.tx_dut.get_charge_inductor
        charge_inductor_osc = self.get_charge_inductor
        charging_time = self.tx_dut.pwm_period*self.tx_dut.pwm_burst_cycles
        avg_current = charge_inductor_osc/self.tx_dut.pwm_burst_cycles/self.tx_dut.pwm_period
        theo_energy_ILmax = 0.5*self.tx_dut.L*self.tx_dut.get_ILmax**2
        theo_energy_ILmeas = 0.5*self.tx_dut.L*self.tx_dut.get_peak_inductor_current**2
        theo_energy_charge_ind = 0.5*charge_inductor_osc*self.tx_dut.Vsupply*self.tx_dut.pwm_burst_cycles
        theo_cap_voltage_ILmax=(2*self.tx_dut.C*theo_energy_ILmax)**0.5
        theo_cap_voltage_ILmeas=(2*self.tx_dut.C*theo_energy_ILmeas)**0.5
        cap_meas_voltage = self.get_max_capacitor_voltage
        energy_cap_meas_voltage = 0.5*self.tx_dut.L*cap_meas_voltage**2
        charge_cap_meas_voltage = self.tx_dut.C*cap_meas_voltage

        charge_efficiency = energy_cap_meas_voltage/theo_energy_ILmeas
        peak_laser_current = self.get_peak_laser_current
        width_laser_current = self.get_width_laser_current
        width_laser_PIN = self.get_width_laser_PIN
        area_laser_current = self.get_area_laser_current
        parasitic_L=(1.5*width_laser_current/np.pi)**2/self.tx_dut.C

        Is = self.laser_fit_coeff[0]
        N = self.laser_fit_coeff[1]
        Rs = self.laser_fit_coeff[2]
        laser_voltage = N*0.026*np.log((peak_laser_current+Is)/Is) +Rs*peak_laser_current
        elect_charge_pulse = 3*np.pi*peak_laser_current*width_laser_current
        energy_laser_pulse_sin = elect_charge_pulse*laser_voltage
        energy_laser_pulse_area = area_laser_current*laser_voltage
        discharge_efficiency_sin = energy_laser_pulse_sin/energy_cap_meas_voltage
        discharge_efficiency_area = energy_laser_pulse_area/energy_cap_meas_voltage

        #write all the data in matrix form to be written in text file
        self.meas_list.append(self.tx_dut.Vsupply)
        self.meas_list.append(self.tx_dut.pwm_burst_cycles)
        self.meas_list.append(self.tx_dut.L)
        self.meas_list.append(self.tx_dut.get_ILmax)
        self.meas_list.append(self.get_peak_inductor_current)
        self.meas_list.append(self.tx_dut.pwm_on)
        self.meas_list.append(self.tx_dut.pwm_period)
        self.meas_list.append(charging_time)
        self.meas_list.append(theo_charge_ind)
        self.meas_list.append(charge_inductor_osc)
        self.meas_list.append(avg_current)
        self.meas_list.append(self.tx_dut.trg_on)
        self.meas_list.append(self.tx_dut.trg_period)
        self.meas_list.append(theo_energy_ILmax)
        self.meas_list.append(theo_energy_ILmeas)
        self.meas_list.append(theo_energy_charge_ind)
        self.meas_list.append(self.tx_dut.C)
        self.meas_list.append(theo_cap_voltage_ILmax)
        self.meas_list.append(theo_cap_voltage_ILmeas)
        self.meas_list.append(cap_meas_voltage)
        self.meas_list.append(energy_cap_meas_voltage)
        self.meas_list.append(charge_cap_meas_voltage)

        self.meas_list.append(charge_efficiency)
        self.meas_list.append(peak_laser_current)
        self.meas_list.append(width_laser_current)
        self.meas_list.append(width_laser_PIN)
        self.meas_list.append(parasitic_L)
        self.meas_list.append(area_laser_current)
        self.meas_list.append(laser_voltage)
        self.meas_list.append(elect_charge_pulse)
        self.meas_list.append(discharge_efficiency_sin)
        self.meas_list.append(discharge_efficiency_area)


        log_data(self.meas_filename, self.meas_list)

    def init_tx_drv(self):
        self.tx_drv.recall_setup_from_memory(3)
        time.sleep(1)

        # time resolution depends from the clock resolution of the mainboard
        time_resolution = self.tx_dut.clock_period
        self.set_pwm_risetime(time_resolution)
        self.set_pwm_falltime(time_resolution)
        self.set_trg_risetime(time_resolution)
        self.set_trg_falltime(time_resolution)

        self.set_pwm_period(self.tx_dut.pwm_period)
        self.set_pwm_width(self.tx_dut.pwm_on)

        pwm_cyc = self.pwm_burst_cycles*self.tx_dut.laser_pulses
        self.set_pwm_cycle(pwm_cyc)
        self.set_pwm_delay(0)

        self.set_trg_cycle(self.tx_dut.laser_pulses)
        trg_period = self.tx_dut.pwm_period*self.pwm_burst_cycles
        self.set_trg_period(trg_period)
        self.set_trg_width(self.tx_dut.trg_on)
        trg_delay = trg_period-self.tx_dut.pwm_off/2-self.tx_dut.trg_on/2
        self.set_trg_delay(trg_delay)

    def set_driving_mode_tx_drv(self):
        outstr='\nInsert PWM ON time[%3.3e]: '% self.tx_dut.pwm_on
        lrf_tx.get_input(self.tx_dut, 'pwm_on', outstr, 'f')
        self.set_pwm_width(self.tx_dut.pwm_on)

        outstr='\nInsert PWM period[%3.3e]: '% self.tx_dut.pwm_period
        lrf_tx.get_input(self.tx_dut, 'pwm_period', outstr, 'f')
        self.set_pwm_period(self.tx_dut.pwm_period)

        pwm_cyc = self.pwm_burst_cycles*self.tx_dut.laser_pulses
        self.set_pwm_cycle(pwm_cyc)
        self.set_pwm_delay(0)

        self.set_trg_cycle(self.tx_dut.laser_pulses)
        trg_period = self.tx_dut.pwm_period*self.pwm_burst_cycles
        self.set_trg_period(trg_period)
        self.set_trg_width(self.tx_dut.trg_on)
        trg_delay = trg_period-self.tx_dut.pwm_off/2-self.tx_dut.trg_on/2
        self.set_trg_delay(trg_delay)


    def measure_energy(self):
        self.set_driving_mode_tx_drv()
        self.set_pwm_output_on()
        self.set_trg_output_on()
        self.shoot()
        self.collect_data()
        self.set_pwm_output_off()
        self.set_trg_output_off()

    def init_report(self):
        self.log_directory = './HistoryLogs/'
        time_filename = timeStamped('_')
        self.log_filename = self.log_directory+time_filename+'log.txt'
        sys.stdout = MyLogOutput(self.log_filename)
        print "  --> log_file: `%s'" % self.log_filename
        self.meas_filename = self.log_directory+time_filename+'meas.txt'

        self.log_file = open(self.log_filename,'a')
        self.meas_file = open(self.meas_filename,'a')
        log_header = 'LaserEnergyTset Log starts @:'+str(datetime.datetime.now())
        print log_header
        self.meas_file.write(log_header)
        self.meas_file.write('\nSupply Voltage, Number of pulses, Induct, AP015 Peak Supply Current,' \
                       'Electrical PWM width, PWM Period, Total Inductor Charge,' \
                       'Electrical TRG pulse width, TRG Period, Nominal Caps,' \
                       'MeasCaps voltages, Peak Laser Current Probe, Current probe pulse width,' \
                       'Current pulse area, PIN optical pulse width\n')
        self.meas_file.close()
        #print_screen oscilloscope
        self.prtsc_filename = self.log_directory+time_filename+'tx'



if __name__ == "__main__":

    myTset = LaserEnergyTset()
    myTset.init_report()

    myTset.measure_energy()
    myTset.collect_data()
