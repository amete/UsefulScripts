#!/usr/bin/python

# brief  : Class to do PDG rounding as explained in Phys. Rev. D 86, 010001 (2012)
# author : Alaettin Serhan Mete (amete@cern.ch)
# date   : April, 2014
# notes  : Be careful and use at your own expense...

from math import *
from decimal import *

# Function to round x into n significant digits
def round_to_n(x,n):
    return round(x, -int(floor(log10(x))) + (n - 1))

# Function to find factor  
def find_factor(x):
    digits = int(log10(x))
    if(x>1): return digits+1
    else   : return digits

# Function to find n highest order digits
def find_hod_n(x,n):
    digits =  find_factor(x)
    return int(x*pow(10,n-digits))

# Function to remove non-significant trailing zeros
def remove_zeros(mean,error):
    if ((mean -int(mean) ) == 0 and mean  >= 1.0 and
        (error-int(error)) == 0 and error >= 1.0): 
        return (int(mean),int(error))
    else:
        return (mean,error)

# Function to do the rounding
def pdg_round(mean,error):
    # Find three first three significant digits
    threeDigitErrorValue = find_hod_n(error,3)
    # Set the number of significant digits to round the values 
    roundValue      = 2
    if  ( threeDigitErrorValue > 354 
      and threeDigitErrorValue < 950 ): roundValue = 1
    elif( threeDigitErrorValue > 950 ): error = pow(10,ceil(log10(error))/log10(10))
    # Round the error 
    newError = round_to_n(error,roundValue)
    # Find the new mean
    factor   = find_factor(error) 
    newMean = (round(float(mean)/pow(10,factor),roundValue)*pow(10,factor))
    # Match the precision of the mean w/ the error
    # There might be a possible limitation when the mean precision is lower then error precision
    # I'm not quite sure if this really happens 
    newMean = float(Decimal(str(newMean)).quantize(Decimal(str(newError))))
    # Remove unnecessary trailing zeros
    return remove_zeros(newMean,newError)

# Print helper
def printHelper(array):
    (newMean, newError) = pdg_round(array[0],array[1])
    print "%10s +/- %10s ===>>> %10s +/- %10s" % (array[0],array[1],newMean,newError)

# Print examples to test the logic
if __name__=='__main__' :
    print "============================================================="
    print "Printing examples in PDG & Tables 1,2 of ATL-COM-GEN-2014-006"
    print "============================================================="
    for values in [ (0.827 ,0.119 ),
                    (0.827 ,0.367 ),
                    (0.9441,0.119 ),
                    (0.9441,0.367 ),
                    (0.9441,0.967 ),
                    (0.9441,0.0632),
                    (0.9441,1.0632),
                    (0.9441,9.0632),
                    (0.9441,9.6632),
                    (191819,17    ),
                    (191819,17891 ),
                    (191819,37891 ),
                    (191819,97891 ),
                  ] : printHelper(values)
    print "============================================================="
