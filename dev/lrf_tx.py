# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:22:43 2012

@author: tricc
"""

#evaluate component of main loop of trasmitter
#import debug_msg
import numpy as np
import matplotlib.pyplot as plt

class GenericLRFTx(object):
    def __init__(self):
        #mainboard parameters
        self.clock_period = 33e-9
        self.Vsupply=5.0
        #inductor parameters
        self.L=680e-6
        self.ILsat=.7
        #capacitor parameters
        self.C=300e-9
        self.Lpar=17e-9
        self.VDSmax=55
        self.Vc0=self.Vsupply

        #parameter circuit section
        self.w0=get_w0(self)
        self.Z0=get_Z0(self)
        self.pulsewidth=get_pulsewidth(self)

        #TRG parameters
        self.trg_voh=3.3 #voltage output high 3.3V
        self.trg_vol=0 #voltage output low 0V
        self.trg_on=2*self.pulsewidth
        self.trg_period=112e-6
        self.trg_delay=110e-6

        #PWM parameters
        self.pwm_voh=3.3 #voltage output high 3.3V
        self.pwm_vol=0 #voltage output low 0V
        self.pwm_on=84e-6
        self.pwm_off=26e-6
        self.pwm_period=(self.pwm_on+self.pwm_off)
        self.pwm_delay=0

        self.pwm_burst_cycles=1
        self.k=range(1, self.pwm_burst_cycles+1)


        self.trg_burst_cycles=1
        self.laser_pulses=7680

        self.pwm_on_max= get_pwm_on_max(self)
        self.pwm_off_max= get_pwm_off_max(self)
        self.pwm_cycles_max= get_pwm_cycles_max(self)

        self.ILmax=get_ILmax(self)
        self.Vc=[]
        self.pwm_off_fx=[]
        self.pwm_off_fxapprox=[]
        self.Vc, self.pwm_off_fx, self.pwm_off_fxapprox = get_pwm_off_variation(self)
        self.charge_pattern=create_analog_charge_pattern_gen(self)

    def update(self):
        #parameter circuit section
        self.w0=get_w0(self)
        self.Z0=get_Z0(self)
        self.pwm_period=(self.pwm_on+self.pwm_off)

        self.pwm_on_max= get_pwm_on_max(self)
        self.pwm_off_max= get_pwm_off_max(self)
        self.pwm_cycles_max= get_pwm_cycles_max(self)
        self.k=range(1, self.pwm_burst_cycles+1)
        self.ILmax=get_ILmax(self)
        self.Vc=[]
        self.pwm_off_fx=[]
        self.pwm_off_fxapprox=[]
        self.Vc, self.pwm_off_fx, self.pwm_off_fxapprox = get_pwm_off_variation(self)
        self.charge_pattern=create_analog_charge_pattern_gen(self)

def create_vector21_tx(tx_obj):
        #mainboard parameters
    tx_obj.clock_period = 33e-9
    tx_obj.Vsupply=5.0
    #inductor parameters
    tx_obj.L=680e-6
    tx_obj.ILsat=.7
    #capacitor parameters
    tx_obj.C=300e-9
    tx_obj.VDSmax=55
    tx_obj.Vc0=tx_obj.Vsupply

    #PWM parameters
    tx_obj.pwm_on=84e-6
    tx_obj.pwm_off=26e-6
    tx_obj.pwm_burst_cycles=1

   #TRG parameters
    tx_obj.trg_on=300e-9
    tx_obj.trg_period=112e-6
    tx_obj.trg_burst_cycles=1
    tx_obj.laser_pulses=7680
    tx_obj.update()

    return tx_obj

def create_xm25_tx(tx_obj):
    #mainboard parameters
    tx_obj.clock_period = 33e-9
    tx_obj.Vsupply=5.8
    #inductor parameters
    tx_obj.L=1000e-6
    tx_obj.ILsat=.7
    #capacitor parameters
    tx_obj.C=300e-9
    tx_obj.VDSmax=100
    tx_obj.Vc0=tx_obj.Vsupply

    #PWM parameters
    tx_obj.pwm_on=84e-6
    tx_obj.pwm_off=26e-6
    tx_obj.pwm_burst_cycles=1
   #TRG parameters
    tx_obj.trg_on=300e-9
    tx_obj.trg_period=112e-6
    tx_obj.trg_burst_cycles=1
    tx_obj.laser_pulses=7680
    tx_obj.update()

    return tx_obj

def create_enh_tx(tx_obj):
    #mainboard parameters
    tx_obj.clock_period = 10e-9
    tx_obj.Vsupply=5
    #inductor parameters
    tx_obj.L=10e-6
    tx_obj.ILsat=1
    #capacitor parameters
    tx_obj.C=9.4e-9
    tx_obj.VDSmax=160
    tx_obj.Vc0=tx_obj.Vsupply

    #PWM parameters
    tx_obj.pwm_on=2.5e-6
    tx_obj.pwm_off=1.5e-6
    tx_obj.pwm_burst_cycles=22

   #TRG parameters
    tx_obj.trg_on=300e-9
    tx_obj.trg_period=112e-6
    tx_obj.trg_burst_cycles=1
    tx_obj.laser_pulses=7680
    tx_obj.update()

    return tx_obj

def get_input(obj, dest, str, flag):
    inp = raw_input(str)
    if flag=='f':
        try:
            setattr(obj, dest, float(inp))
        except ValueError:
            pass
    if flag=='i':
        try:
            setattr(obj, dest, int(inp))
        except ValueError:
            pass


def create_custom_tx(tx_obj):
    print "!!!INSERT VALUE OR PRESS ENTER TO ACCEPT DEFAULT!!!"
    #mainboard parameters
    str='\nInsert DSP clock period[%3.3e]: ' % tx_obj.clock_period
    get_input(tx_obj, 'clock_period', str, 'f')

    str='\nInsert supply voltage[%3.3e]: ' % tx_obj.Vsupply
    get_input(tx_obj, 'Vsupply', str, 'f')

    str='\nInsert number of laser pulses[%d]: ' % tx_obj.laser_pulses
    get_input(tx_obj, 'laser_pulses', str, 'f')

    #inductor parameters
    str='\nInsert charge inductor[%3.3e]: ' % tx_obj.L
    get_input(tx_obj, 'L', str, 'f')

    str='\nInsert inductor saturation current[%3.3e]: ' % tx_obj.ILsat
    get_input(tx_obj, 'ILsat', str, 'f')

    #PWM parameters
    print "\nMax theory PWM ON time[s] %3.3e" % get_pwm_on_max(tx_obj)
    str='\nInsert PWM ON time[%3.3e]: ' % tx_obj.pwm_on
    get_input(tx_obj, 'pwm_on', str, 'f')

    print "\nTheory Inductor peak current[A] %3.3e" % get_ILmax(tx_obj)
    #capacitor parameters
    str='\nInsert capacitor[%3.3e]: ' % tx_obj.C
    get_input(tx_obj, 'C', str, 'f')

    print "\nMin theory PWM OFF time allowed for DCM[s] %3.3e" % get_pwm_off_max(tx_obj)
    str='\nInsert PWM OFF time[%3.3e]: ' % tx_obj.pwm_off
    get_input(tx_obj, 'pwm_off', str, 'f')

    str='\nInsert max capacitor voltage[%3.3e]: ' % tx_obj.VDSmax
    get_input(tx_obj, 'VDSmax', str, 'f')

    print "\nMax capacitor energy[J] %3.3e" % get_energy_capacitor_VDSmax(tx_obj)
    print_charge_pattern(tx_obj)

    str='\nInsert number of PWM pulses[%d]: ' % tx_obj.pwm_burst_cycles
    get_input(tx_obj, 'pwm_burst_cycles', str, 'i')

    #TRG parameters
    str='\nInsert TRG pulsewidh[%3.3e]: ' % tx_obj.trg_on
    get_input(tx_obj, 'trg_on', str, 'f')

    str='\nInsert TRG period[%3.3e]: ' % tx_obj.trg_period
    get_input(tx_obj, 'trg_period', str, 'f')

    tx_obj.Vc0=tx_obj.Vsupply

    #parameter circuit section
    tx_obj.w0=get_w0(tx_obj)
    tx_obj.Z0=get_Z0(tx_obj)
    tx_obj.pwm_period=(tx_obj.pwm_on+tx_obj.pwm_off)

    tx_obj.pwm_on_max= get_pwm_on_max(tx_obj)
    tx_obj.pwm_off_max= get_pwm_off_max(tx_obj)
    tx_obj.pwm_cycles_max= get_pwm_cycles_max(tx_obj)
    tx_obj.Vc=[]
    tx_obj.pwm_off_fx=[]
    tx_obj.pwm_off_fxapprox=[]
    tx_obj.k=range(1, get_max_pwm_cycles_VDSmax(tx_obj)+1)
    tx_obj.Vc, tx_obj.pwm_off_fx, tx_obj.pwm_off_fxapprox = get_pwm_off_variation(tx_obj)

    print "\nMax PWM pulses limit by VDSmax[s] %3.3e" % get_max_pwm_cycles_VDSmax(tx_obj)
    print_charge_pattern(tx_obj)

    print "\nMax PWM pulses limit by TRG time[s] %3.3e" % get_max_pwm_cycles_trg_period(tx_obj)
    tx_obj.k=range(1, tx_obj.pwm_burst_cycles+1)

    tx_obj.Vc=[]
    tx_obj.pwm_off_fx=[]
    tx_obj.pwm_off_fxapprox=[]
    tx_obj.Vc, tx_obj.pwm_off_fx, tx_obj.pwm_off_fxapprox = get_pwm_off_variation(tx_obj)
    tx_obj.charge_pattern=create_analog_charge_pattern_gen(tx_obj)

    print_charge_pattern(tx_obj)

    return tx_obj

def create_analog_charge_pattern_gen(tx_obj):
    # time resolution depends from the clock resolution of the mainboard
    time_resolution = tx_obj.clock_period
    # we start to build the pattern normaliyed to counter frequency
    charge_pattern =  np.zeros((1,), dtype=np.int)
    for kk in range(len(tx_obj.pwm_off_fx)):
        thigh_rel = int(tx_obj.pwm_on / time_resolution)
        thigh_vec = tx_obj.pwm_voh*np.ones((thigh_rel,), dtype=np.int)
        charge_pattern = np.concatenate((charge_pattern, thigh_vec), axis=0)
        tlow_rel = int(tx_obj.pwm_off_fx[kk] / time_resolution)
        tlow_vec = np.zeros((tlow_rel,), dtype=np.int)
        charge_pattern = np.concatenate((charge_pattern, tlow_vec), axis=0)

    #plt.plot(charge_pattern)
    #plt.show()
    return charge_pattern

def get_driving_mode(tx_obj):
    # time resolution depends from the clock resolution of the mainboard
    time_resolution = tx_obj.clock_period
    print "\ndigital dt:%s" % time_resolution
    print "\nrise time:%s" % time_resolution
    print "\nfall time:%s" % time_resolution

    print "\nPWM high value:%s" % tx_obj.pwm_voh
    print "\nPWM low value:%s" % tx_obj.pwm_vol
    print "\nPWM width:%s" % tx_obj.pwm_on
    print "\nPWM period:%s" % tx_obj.pwm_period
    print "\nPWM delay:%s" % tx_obj.pwm_delay

    print "\nTRG high value:%s" % tx_obj.trg_voh
    print "\nTRG low value:%s" % tx_obj.trg_vol
    print "\nTRG width:%s" % tx_obj.trg_on
    print "\nTRG period:%s" % tx_obj.trg_period

def get_pwm_off_variation(tx_obj):
    Vsupply=np.float64(tx_obj.Vsupply)
    Vc0=np.float64(tx_obj.Vc0)
    ton=np.float64(tx_obj.pwm_on)
    L=np.float64(tx_obj.L)
    C=np.float64(tx_obj.C)
    w0=np.float64(tx_obj.w0)
    Z0=np.float64(tx_obj.Z0)
    IL0=np.float64(tx_obj.ILsat)

    Vc=[]
    pwm_off=[]
    pwm_off_approx=[]

    for kk in tx_obj.k:
        #iL=(IL0)*cos(w0*t)+(Vsupply-Vc0)/Z0*sin(w0*t)
        Vc_k=Vsupply*(ton*(kk/L/C)**.5)+Vc0
        if kk == 1:
            pwm_off_k = np.pi/2/w0
            pwm_off_approx_k=np.pi/2/w0
        else:
            pwm_off_k=np.arctan(IL0*Z0/(-Vc0+Vc_k))/w0
            pwm_off_approx_k=((IL0*Z0)/(ton*Vc0*w0**2)/(kk**.5))
        Vc.append(Vc_k)
        pwm_off.append(pwm_off_k)
        pwm_off_approx.append(pwm_off_approx_k)

    return Vc, pwm_off, pwm_off_approx
   #iL(k)=(IL0)*ones(size(Vc(k)))*cos(w0*t)+(Vsupply-Vc(k))./Z0*sin(w0*t)
        #vc=+(Vsupply-Vc0)/Z0(IL0)*cos(w0*t)+(Vsupply-Vc0)/Z0*sin(w0*t)

#    plt.plot(k, toff)
#    plt.show()
    return 0

def get_pwm_off_max(tx_obj):
    pwm_off_max=np.pi/2/get_w0(tx_obj)
    return pwm_off_max

def get_pwm_on_max(tx_obj):
    pwm_on_max=tx_obj.ILsat*tx_obj.L/tx_obj.Vsupply
    return pwm_on_max

def get_max_pwm_cycles_VDSmax(tx_obj):
    pwm_cycles_max=int(((tx_obj.VDSmax-tx_obj.Vc0)/(tx_obj.Vsupply*tx_obj.w0*tx_obj.pwm_on))**2)
    return pwm_cycles_max

def get_VDSmax_pwm_cycles(tx_obj):
    Vcf=tx_obj.Vsupply*(tx_obj.pwm_on*(tx_obj.pwm_burst_cycles/tx_obj.L/tx_obj.C)**.5)+tx_obj.Vc0
    return Vcf

def get_max_pwm_cycles_trg_period(tx_obj):
    pwm_cycles_max=int(tx_obj.trg_period/(tx_obj.pwm_period))
    return pwm_cycles_max

def get_pwm_cycles_max(tx_obj):
    pwm_VDSmax = get_max_pwm_cycles_VDSmax(tx_obj)
    pwm_trgmax = get_max_pwm_cycles_trg_period(tx_obj)
    if  pwm_VDSmax < pwm_trgmax:
        return pwm_VDSmax
    else:
        return pwm_trgmax

def get_w0(tx_obj):
    w0=(tx_obj.L*tx_obj.C)**-0.5
    return w0

def get_pulsewidth(tx_obj):
    tpulse=np.pi*(tx_obj.Lpar*tx_obj.C)**0.5/1.5
    return tpulse

def get_Z0(tx_obj):
    Z0=(tx_obj.L/tx_obj.C)**0.5
    return Z0

def get_ILmax(tx_obj):
    ILmax=(tx_obj.Vsupply/tx_obj.L)*tx_obj.pwm_on
    return ILmax

def get_charge_inductor(tx_obj):
    charge=(tx_obj.Vsupply/2/tx_obj.L)*tx_obj.pwm_on**2*tx_obj.pwm_burst_cycles
    return charge

def get_energy_inductor_ILmax(tx_obj):
    energy=.5*tx_obj.L*(get_ILmax(tx_obj))**2
    return energy

def get_energy_capacitor_VDSmax(tx_obj):
    energy=.5*tx_obj.C*tx_obj.VDSmax**2
    return energy

def get_cap_voltage(tx_obj):
    Vsupply=np.float64(tx_obj.Vsupply)
    Vc0=np.float64(tx_obj.Vc0)
    ton=np.float64(tx_obj.pwm_on)
    L=np.float64(tx_obj.L)
    C=np.float64(tx_obj.C)

    Vc=[]

    for kk in tx_obj.k:
        #iL=(IL0)*cos(w0*t)+(Vsupply-Vc0)/Z0*sin(w0*t)
        Vc_k=Vsupply*(ton*(kk/L/C)**.5)+Vc0
        Vc.append(Vc_k)
    return Vc

def check_ccm_mode(tx_obj):
    print debug_msg.TBD_MSG

def print_charge_pattern(tx_obj):
    print '\nPULSE\t\t TIME\t\t PWM_OFF\t\t VCAP_FIN\n'
    for item in range(len(tx_obj.k)):
        print "%d\t\t %2.2e\t\t %2.2e\t\t %3.2f\n" % (tx_obj.k[item], tx_obj.k[item]*(tx_obj.pwm_period), tx_obj.pwm_off_fx[item], tx_obj.Vc[item])

if __name__ == "__main__":
    dut=create_custom_tx(GenericLRFTx())
    inp = raw_input("PRESS ENTER to exit...")
#    print_charge_pattern(dut)
#    print dut.pwm_cycles_max
#    plt.plot(dut.k, dut.pwm_off_fx)
#    plt.show()
