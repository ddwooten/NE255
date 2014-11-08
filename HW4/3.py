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
sig_a = sig_t - sig_s0 
logging.debug( 'The abs cross section is ' + str( sig_a ) )
#Cross section array
sig_array = [ sig_t , sig_s0 , sig_s1 , sig_a ]

#Lets initilize our holding arrays
collisions = np.zeros( h )
absorptions = np.zeros( h )
leakage = np.zeros( 2 )

#This function will follow the lifespan of one neutron
def Lifetime( col_counter , abs_counter , leak_counter , xs_array , \
                xs_array , cell_width , start_pos() , angle() , \
                distance() , leakage() , collide() , col_type() , \
                location() , new_angle() , cep() ):
    '''This function caries a neutron through its lifespan'''
    cep()
    logging.debug( 'Starting new neutron history' )
#This is a boolean that will help us track life/death
    alive = TRUE
    cep()
    logging.debug( 'Neutron is alive: ' + str( alive ) )
#This is a boolean that will help us track leakage
    inside = TRUE
    cep()
    logging.debug( 'Neutron is inside: ' + str( inside ) )
#Start the neutron off with a position and an angle 
    pos = start_pos()
    cep()
    logging.debug( 'Neutron is starting at: ' + str( pos ) )
    mu = angle()
    cep()
    logging.debug( 'Neutron has angle: ' + str( mu ) )
#Counter for number of loops
    num_col = 0
#Here we begin the tracking loop
#While the neutron is both not absorbed and not leaked
    while ( inside and alive ):
        cep()
        logging.debug( 'Tracking collision number: ' + str( num_col ) )
#Get the total distance traveled
        dis = distance()
        cep()
        logging.debug( 'Neutron is traveling distance: ' + \
            str( dis ) )
        cep()
        logging.debug( 'Projected distance is: ' + str( dis * mu ) )
#Project onto the x axis
        pos = pos + dis * mu
        cep()
        logging.debug( 'New position is: ' + str( pos ) )
#Check for leakage
        cep()
        logging.debug( 'Checking for leakage' )
        leakage( pos , leak_counter , inside )
        logging.debug( 'Neutron is inside: ' + str( inside ) )
        logging.debug( 'Neutron is alive: ' + str( alive ) )
#If the neutron didn't leak, collide it
        cep()
        logging.debug( 'Colliding neutron if alive:' )
        logging.debug( 'Parameters before collision: ' )
        logging.debug( 'Incoming angle is: ' + str( mu ) )
        if alive: collide( pos , mu , col_counter, abs_counter , \
           alive, angle() , col_type() , location() , xs_array , cell_width\
           , new_angle() )
        cep()
        logging.debug( 'Neutron parameters post collision: ' )
        logging.debug( 'Outgoing angle is: ' + str( mu ) )
        cep()
        logging.debug( 'Neutron is alive: ' + str( alive ) )
        logging.debug( 'Neutron is inside: ' + str( inside ) )
#Increment the collision number
        num_col += 1
    return()

#This function will handle colliding neutrons
def collide( position , MU , col , absor , existance , angle() \
                , col_type() , location() , xs , width ):
    '''This function collides neutrons and hanldes the aftermath'''
#Determine the type of collision
    collision = col_type( xs )
#Determine the spatial bin this occured in
    spatial_bin = location( position , width )
#If the collision was a scatter
    if collision > 0:
#Tabulate the collision 
        col[ spatial_bin ] += 1
#Get a new angle post scatter
        MU = new_angle( MU , xs )
#If the collision was an abosrption
    else:
#Tabulate the absorption
        absor[ spatial_bin ] += 1
#And "kill" the  nuetron
        existance = FALSE  
    return()

#This function calculates an outgoing angle post scattering
def new_angle( incoming , x_sec ):
    '''This function calculates an outgoing aniso angle'''
#We define the average scattering angle
    mu_bar = x_sec[ 2 ] / x_sec[ 1 ]
#Calculate the new mu post scattering
    new_mu = -1 + np.sqrt( 1 - 3 * incoming * mu_bar * [ \
        2 * ( 1 - 2 * np.random.random(1) ) -3 * incoming * \
        mu_bar ] ) / ( 3 * incoming * mu_bar )
    return( new_mu )

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
#Random number between 0 and 1
    quanta = np.random.random( 1 )
#If said rand num is less than the ratio of the abs
#   cross section to the total, the collision
#   was an absorption
    if quanta <= csx_array[ 3 ] / csx_array[ 0 ]:
        col_type = int( 0 )
#Otherwise it was a scatter
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
#Easier to assign a negative this way
    sign = np.random.randint( 2 )
#Get a random number between 0 and 1 for angle
    ang = np.random.random( 1 )
#Assign the sign value
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
