#!/usr/bin/python
# Creator: Daniel Wooten
# NE255 HW4 P1 MC Code

import logging as logging
import time as time
import sys as sys
import numpy as np

# Function, refer to docstring for purpose
def cep():
	''' A wrapper to place file seperators in a log file for the
	debug level '''
	logging.debug( "*****************************************************" )
	return()
# Let the user know that the code is running
print "*****************************************************"
print "Pi Approximation CODE BEGIN!"

#Take in the number of samples
N = int( raw_input('Please input the number of samples\n') )

# File names for the log and output files respectively
LogFileName = 'logfile.dat'

OutputFile = 'output.dat'

#Set the log level
LogLevel = 0

# This does some basic config on the log file
logging.basicConfig( filename = LogFileName , format = \
    "[%(levelname)8s] %(message)s" , filemode =\
     'w' , level = LogLevel )
logging.debug( "This is the debug level reporting in" )
logging.info( "This is the info level reporting in " )
logging.warning( "This is the warning level reporting in" )
logging.error( "This is the error level reporting in" )
logging.critical( "This is the critical level reporting in" )

logging.debug( 'The number of samples being run is ' + str(N) )

#Generate the random number arrays and scale them to the problem
rand_x = np.random.rand(N)
rand_y = np.random.rand(N)

#Generate the logical vector of if the point are above or under
#the curve
below_a = rand_y < ( np.sqrt( 1 - ( rand_x**2 ) ) )
below_b = rand_y < ( 1 / ( 1 + rand_x**2 ) )

#Calculate pi approximation
pi_approx_a = 4.0 * sum( below_a ) / float( N )
pi_approx_b = 4.0 * sum( below_b ) / float( N )

#Calculate the relative error
rel_err_a = abs( ( pi_approx_a - np.pi ) / np.pi ) * 100
rel_err_b = abs( ( pi_approx_b - np.pi ) / np.pi ) * 100

#Print the results
print 'The approximated value of pi for a is\n'
print str( pi_approx_a )
print 'With relative error \n'
print str( rel_err_a )
print 'The approximated value of pi for b is \n'
print str( pi_approx_b )
print 'With relative error \n'
print str( rel_err_b )

# Let the user know it has all ended
print "Sn CODE END!!"
print "*************************************************************"
