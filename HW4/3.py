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

#Define cell length
cell_length = 8.0 / float( h )

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
                cell_width , start_pos , angle , \
                distance , leakage , collide , col_type , \
                location , new_angle , cep ):
    '''This function caries a neutron through its lifespan'''
    cep()
    cep()
    logging.debug( 'Starting new neutron history' )
#This is a boolean that will help us track life/death
    alive = True
    cep()
    logging.debug( 'Neutron is alive: ' + str( alive ) )
#This is a boolean that will help us track leakage
    inside = True
    cep()
    logging.debug( 'Neutron is inside: ' + str( inside ) )
#Start the neutron off with a position and an angle 
    pos = start_pos( cep )
    cep()
    logging.debug( 'Neutron is starting at: ' + str( pos ) )
    mu = angle( cep )
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
        dis = distance( xs_array[ 0 ] ,  cep )
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
        leakage( pos , leak_counter , inside , cep)
        logging.debug( 'Neutron is inside: ' + str( inside ) )
        logging.debug( 'Neutron is alive: ' + str( alive ) )
#If the neutron didn't leak, collide it
        cep()
        logging.debug( 'Colliding neutron if alive:' )
        logging.debug( 'Parameters before collision: ' )
        logging.debug( 'Incoming angle is: ' + str( mu ) )
        if alive: collide( pos , mu , col_counter, abs_counter , \
           alive, angle , col_type , location , xs_array , cell_width\
           , new_angle , cep )
        cep()
        logging.debug( 'Neutron parameters post collision: ' )
        logging.debug( 'Outgoing angle is: ' + str( mu ) )
        cep()
        logging.debug( 'Neutron is alive: ' + str( alive ) )
        logging.debug( 'Neutron is inside: ' + str( inside ) )
#Increment the collision number
        num_col += 1
    logging.debug( 'Terminating neutron history' )
    cep()
    cep()
    return()

#This function will handle colliding neutrons
def collide( position , MU , col , absor , existance , angle \
                , col_type , location , xs , width , cep ):
    '''This function collides neutrons and hanldes the aftermath'''
    cep()
    cep()
    logging.debug( 'Entering the colision routine' )
#Determine the type of collision
    collision = col_type( xs , cep )
    cep()
    logging.debug( 'Collision of type: ' + str( collision ) )
#Determine the spatial bin this occured in
    spatial_bin = location( position , width , cep )
    cep()
    logging.debug( 'Spatial bin of: ' + str( spatial_bin ) )
#If the collision was a scatter
    if collision > 0:
        cep()
        logging.debug( 'Collision was a scatter' )
#Tabulate the collision 
        cep()
        logging.debug( 'Collision count before tabulation: ' )
        logging.debug( 'Spatial bin: ' + str( spatial_bin ) \
            + ' has ' + str( col[ spatial_bin ] ) )
        col[ spatial_bin ] += 1
        logging.debug( 'Collision count in bin ' + \
            str( spatial_bin ) + ' now: ' + \
            str( col[ spatial_bin ] ) ) 
#Get a new angle post scatter
        cep()
        logging.debug( 'Incoming angle: ' + str( MU ) )
        MU = new_angle( MU , xs , cep )
        cep()
        logging.debug( 'Outgoing angle: ' + str( MU ) ) 
#If the collision was an abosrption
    else:
#Tabulate the absorption
        cep()
        logging.debug( 'Collision was an absorption' )
        logging.debug( 'Abs count in bin ' + str( spatial_bin )  \
            + ' is: ' + str( absor[ spatial_bin ] ) )
        absor[ spatial_bin ] += 1
        logging.debug( 'Count is now: ' + str( absor[ spatial_bin ] ) )
#And "kill" the  nuetron
        existance = False  
        cep()
        logging.debug( 'Neutron is now alive: ' + str( existance ) )
    logging.debug( 'Leaving the collision function' )
    cep()
    cep()
    return()

#This function calculates an outgoing angle post scattering
def new_angle( incoming , x_sec , cep ):
    '''This function calculates an outgoing aniso angle'''
    cep()
    cep()
    logging.debug( 'Entering the new_angle function' )
#We define the average scattering angle
    mu_bar = x_sec[ 2 ] / x_sec[ 1 ]
#Calculate the new mu post scattering
    new_mu = -1 + np.sqrt( 1 - 3 * incoming * mu_bar * [ \
        2 * ( 1 - 2 * np.random.random(1) ) -3 * incoming * \
        mu_bar ] ) / ( 3 * incoming * mu_bar )
    cep()
    logging.debug( 'Outgoing angle is: ' + str( new_mu ) )
    logging.debug( 'Leaving the new_angle function' )
    cep()
    cep()
    return( new_mu )

#This function determines in which spatial bin an interaction occurs
def location( place , bin_width , cep ):
    '''This function determines in which bin an interaction occurs'''
    cep()
    cep()
    logging.debug( 'Entering the location function' )
    cell = int( math.floor( place / float( bin_width ) ) )
    logging.debug( 'Cell is: ' + str( cell ) )
    logging.debug( 'Leaving the location function' )
    cep()
    cep()
    return( cell )
        
#This function will determine if the neutron leaked
def leakage( location , leak_array , present , cep ):
    '''This function tracks leakage'''
    cep()
    cep()
    logging.debug( 'Entering the leakage function ' )
    logging.debug( 'Location is: ' + str( location ) )
    logging.debug( 'Left leakage is: ' + str( leak_array[ 0 ] ) )
    logging.debug( 'Right leakage is: ' + str( leak_array[ 1 ] ) )
    if location > 8.0: present = False ; leak_array[ 1 ] += 1
    if location < 0.0: present = False ; leak_array[ 0 ] += 1
    cep()
    logging.debug( 'Neutron is inside: ' + str( present ) )
    logging.debug( 'Left leakage is: ' + str( leak_array[ 0 ] ) )
    logging.debug( 'Right leakage is: ' + str( leak_array[ 1 ] ) )
    logging.debug( 'Leaving the leakage function' )
    cep()
    cep()
    return()

#This function determines the collision type
def col_type( csx_array , cep ):
    '''Ths function determines the collision type'''
#Random number between 0 and 1
    cep()
    cep()
    logging.debug( 'Entering the col_type function' )
    quanta = np.random.random( 1 )
    cep()
    logging.debug( 'Collision random is: ' + str( quanta ) )
#If said rand num is less than the ratio of the abs
#   cross section to the total, the collision
#   was an absorption
    logging.debug( 'Threshold for abs is: ' + \
        str( csx_array[ 3 ] / csx_array[ 0 ] ) )
    cep()
    if quanta <= csx_array[ 3 ] / csx_array[ 0 ]:
        col_type = int( 0 )
        logging.debug( 'Collision type is: ' +\
            str( col_type ) )
#Otherwise it was a scatter
    else:
        col_type = int( 1 )
        logging.debug( 'Collision type is: ' +\
           str( col_type ) )
    logging.debug( 'Leaving the col_type function' )
    cep()
    cep()
    return( col_type )

#This function generates a start position for our neutron
def start_pos( cep ):
    '''This function generates a start pos for our neutron'''
    cep()
    cep()
    logging.debug( 'Entering the start_pos function' )
    pos = np.random.random( 1 ) * 4.0
    cep()
    logging.debug( 'The starting position is ' + str( pos ) )
    logging.debug( 'Leaving the start_pos function' )
    cep()
    cep()
    return( pos )

#This function generates a random angle on (-1,1)
def angle( cep ):
    '''This function generates a random angle on (-1,1)'''
    cep()
    cep()
    logging.debug( 'Entering the angle function' )
#Easier to assign a negative this way
    sign = np.random.randint( 2 )
    logging.debug( 'Sign has value: ' + str( sign ) )
#Get a random number between 0 and 1 for angle
    ang = np.random.random( 1 )
    logging.debug( 'Angle has value: ' + str( ang ) )
#Assign the sign value
    if sign == 0: ang = ang * -1.0
    logging.debug( 'Angle is: ' + str( ang ) )
    logging.debug( 'Leaving the angle function' )
    cep()
    cep()
    return( ang )

#This function will give us the distance our neutron travels
def distance( t_sig , cep ):
    '''This function calculates distance to next collision'''
    cep()
    cep()
    logging.debug( 'Entering the distance function' )
    dis = -np.log( np.random.random( 1 ) ) / t_sig
    logging.debug( 'The calculated distance is ' + str( dis ) )
    logging.debug( 'Leaving the distance function' )
    cep()
    cep()
    return( dis )

#Lets begin our neutron histories loop
for i in range( N ):
     Lifetime( collisions , absorptions , leakage , sig_array , \
                    cell_length , start_pos , angle , \
                    distance , leakage , collide , col_type , \
                    location , new_angle , cep )


# Let the user know it has all ended
print "Sn CODE END!!"
print "*************************************************************"
