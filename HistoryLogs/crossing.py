from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def crossings(time, signal, level = 0):
    """CROSSING find the crossings of a given level of a signal
    #   ind = CROSSING(S) returns an index vector ind, the signal
    #   S crosses zero at ind or at between ind and ind+1
    #   [ind,t0] = CROSSING(S,t) additionally returns a time
    #   vector t0 of the zero crossings of the signal S. The crossing
    #   times are linearly interpolated between the given times t
    #   [ind,t0] = CROSSING(S,t,level) returns the crossings of the
    #   given level instead of the zero crossings
    """

    t= time
    S = signal
    # always search for zeros. So if we want the crossing of
    # any other threshold value "level", we subtract it from
    # the values and search for zeros.
    S   = S - level

    # first look for exact zeros
    ind0 = np.nonzero(S==0)

    # and pick the associated time values
    t0 = t[ind0]
    # then look for zero crossings between data points rising edge
    ind1 = np.nonzero((S[:-1]> 0) & (S[1:] < 0))

    # then look for zero crossings between data points falling edge
    ind2 = np.nonzero((S[:-1]< 0) & (S[1:] > 0))

    # bring exact zeros and "in-between" zeros together
    indnz = np.concatenate((ind1[0], ind2[0]), axis=1)
    indnz.sort()
    

#    if imeth is 'linear':
#    # linear interpolation of crossing
#        for ii in range(len(t0)):
#            if np.abs(S[ind[ii]]) > np.spacing(S[ind[ii]]):
#                # interpolate only when data point is not already zero
#                NUM = (t[ind[ii]+1] - t[ind[ii]])
#                DEN = (S[ind[ii]+1] - S[ind[ii]])
#                DELTA =  NUM / DEN
#                t0[ii] = t0[ii] - S[ind[ii]] * DELTA
#                # I'm a bad person, so I simply set the value to zero
#                # instead of calculating the perfect number ;)
#                s0[ii] = 0

    # More accurate, using linear interpolation to find intersample
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crosstime = [t[i] - S[i]*(t[i+1]-t[i])/(S[i+1]-S[i]) for i in indnz]
    timevect = np.concatenate((t0, crosstime), axis=1)
    timevect.sort() 
    idxvect = np.concatenate((ind0[0], indnz), axis=1)
    idxvect.sort()                   
    return idxvect, timevect

def main():
    newtime = np.arange(-2, 2.5, .25)
    coeff_par = [1, 0, -1] #x^2-1
    ypar = np.polyval(coeff_par, newtime)
    idxvect, timevect = crossings(newtime, ypar, 2)
    print idxvect, timevect
    #calculate the horizontal position of max for a general parabola
    #place into point [0, 1, 2] -> tmax = -b/2a on x = [0, 1, 2]
    plt.plot(newtime, ypar)  
    plt.show()

if __name__ == "__main__":
    main()
