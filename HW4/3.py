#!/usr/bin/python
# Creator: Daniel Wooten
# NE255 HW4 P3 MC Code

import logging as logging
import time as time
import sys as sys
import numpy as np
import math as math

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

#Define the number of spatial bins
h = 100

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

#Define some quantities
sig_t = 1
logging.debug( 'The total cross section is ' + str( sig_t ) )
sig_s0 = 0.8
logging.debug( 'The iso scattering cross section is ' \
    + str( sig_s0 ) )
sig_s1 = 0.2
logging.debug( 'The an-iso scattering cross section is ' \
    + str( sig_s1 ) )
sig_a = sig_t - sig_s0 / np.pi
logging.debug( 'The abs cross section is ' + str( sig_a ) )
sig_array = [ sig_t , sig_s0 , sig_s1 , sig_a ]

#Lets initilize our holding arrays
collisions = np.zeros( h )
absorptions = np.zeros( h )
leakage = np.zeros( 2 )

#This function will follow the lifespan of one neutron
def Lifetime( col_counter , abs_counter , leak_counter , xs_array , \
                xs_array , cell_width , start_pos() , angle() , \
                distance() , leakage() , collide() , col_type() , \
                location() ):
    '''This function caries a neutron through its lifespan'''
#This is a boolean that will help us track life/death
    alive = TRUE
#This is a boolean that will help us track leakage
    inside = TRUE
    pos = start_pos()
    mu = angle()
#Here we begin the tracking loop
    while ( inside and alive ):
        dis = distance()
        pos = pos + dis * mu
        leakage( pos , leak_counter , inside )
        if alive: collide( pos , mu , col_counter, abs_counter , \
           alive, angle() , col_type() , location() , xs_array , cell_width )
    return()

#This function will handle colliding neutrons
def collide( position , MU , col , absor , existance , angle() \
                , col_type() , location() , xs , width ):
    '''This function collides neutrons and hanldes the aftermath'''
    collision = col_type( xs )
    spatial_bin = location( position , width )
    if collision > 0: 
        col[ spatial_bin ] += 1
        MU = angle()
    else:
        absor[ spatial_bin ] += 1
        existance = FALSE  
    return()

#This function determines in which spatial bin an interaction occurs
def location( place , bin_width ):
    '''This function determines in which bin an interaction occurs'''
       cell = int( math.floor( place / float( bin_width ) ) )
       return( cell )
        
#This function will determine if the neutron leaked
def leakage( location , leak_array , present ):
    '''This function tracks leakage'''
    if location > 8.0: present = FALSE ; leak_array[ 1 ] += 1
    if location < 0.0: present = FALSE ; leak_array[ 0 ] += 1
    return()

#This function determines the collision type
def col_type( csx_array ):
    '''Ths function determines the collision type'''
    quanta = np.random.random( 1 )
    if quanta <= csx_array[ 3 ] / csx_array[ 0 ]:
        col_type = int( 0 )
    else:
        col_type = int( 1 )
    return( col_type )

#This function generates a start position for our neutron
def start_pos( cep ):
    '''This function generates a start pos for our neutron'''
    pos = np.random.random( 1 ) * 4.0
    cep()
    logging.debug( 'The starting position is ' + str( pos ) )
    return( pos )

#This function generates a random angle on (-1,1)
def angle( cep ):
    '''This function generates a random angle on (-1,1)'''
    sign = np.random.randint( 2 )
    ang = np.random.random( 1 )
    if sign == 0: ang = ang * -1.0
    cep()
    logging.debug( 'The angle of travel is ' + str( ang )
    return( ang )

#This function will give us the distance our neutron travels
def distance( cep, t_sig ):
    '''This function calculates distance to next collision'''
    dis = -np.log( np.random.random( 1 ) ) / t_sig
    cep()
    logging.debug( 'The calculated distance is ' + str( dis ) )
    return( dis )

#Lets begin our neutron histories loop
for i in range( N )


# Let the user know it has all ended
print "Sn CODE END!!"
print "*************************************************************"
