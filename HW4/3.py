#!/usr/bin/python
# Creator: Daniel Wooten
# NE255 HW4 P3 MC Code

import logging as logging
import time as time
import sys as sys
import numpy as np
import math as math
import pylab as pl

# Function, refer to docstring for purpose
def cep():
	''' A wrapper to place file seperators in a log file for the
	debug level '''
	logging.debug( "*****************************************************" )
	return()

#Function, refer to docstring for purpose
def sep():
    '''A wrapper to visually seperate functions in log files'''
    logging.debug( '//////////////////////////////////////////////////////' )
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

#Lets initilize our holding arrays
collisions = np.zeros( h )
absorptions = np.zeros( h )
leak_array = np.zeros( 2 )

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

#This function will follow the lifespan of one neutron
def Lifetime( col_counter , abs_counter , leak_counter , xs_array , \
                cell_width , start_pos , angle , \
                distance , leakage , collide , col_type , \
                location , new_angle , cep , sep ):
    '''This function caries a neutron through its lifespan'''
    sep()
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
    pos = start_pos( cep , sep )
    cep()
    logging.debug( 'Neutron is starting at: ' + str( pos ) )
    mu = angle( cep , sep )
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
        dis = distance( xs_array[ 0 ] ,  cep , sep )
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
        inside = leakage( pos , leak_counter , inside , cep , sep )
        logging.debug( 'Neutron is inside: ' + str( inside ) )
        logging.debug( 'Neutron is alive: ' + str( alive ) )
#If the neutron didn't leak, collide it
        cep()
        logging.debug( 'Colliding neutron if alive:' )
        logging.debug( 'Parameters before collision: ' )
        logging.debug( 'Incoming angle is: ' + str( mu ) )
        if alive: alive = collide( pos , mu , col_counter, abs_counter , \
           alive, angle , col_type , location , xs_array , cell_width\
           , new_angle , cep , sep )
        cep()
        logging.debug( 'Neutron parameters post collision: ' )
        logging.debug( 'Outgoing angle is: ' + str( mu ) )
        cep()
        logging.debug( 'Neutron is alive: ' + str( alive ) )
        logging.debug( 'Neutron is inside: ' + str( inside ) )
#Increment the collision number
        num_col += 1
    logging.debug( 'Terminating neutron history' )
    sep()
    return()

#This function will handle colliding neutrons
def collide( position , MU , col , absor , existance , angle \
                , col_type , location , xs , width , new_angle , cep , sep ):
    '''This function collides neutrons and hanldes the aftermath'''
    sep()
    logging.debug( 'Entering the colision routine' )
#Determine the type of collision
    collision = col_type( xs , cep , sep )
    cep()
    logging.debug( 'Collision of type: ' + str( collision ) )
#Determine the spatial bin this occured in
    spatial_bin = location( position , width , cep , sep )
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
        MU = new_angle( MU , xs , cep , sep )
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
    sep()
    return( existance )

#This function calculates an outgoing angle post scattering
def new_angle( incoming , x_sec , cep , sep ):
    '''This function calculates an outgoing aniso angle'''
    sep()
    logging.debug( 'Entering the new_angle function' )
#We define the average scattering angle
    mu_bar = x_sec[ 2 ] / x_sec[ 1 ]
#Calculate the new mu post scattering
    new_mu = -1 + math.sqrt( 1 - 3 * incoming * mu_bar * ( \
        2 * ( 1 - 2 * np.random.random(1) ) -3 * incoming * \
        mu_bar ) ) / ( 3 * incoming * mu_bar )
    cep()
    logging.debug( 'Outgoing angle is: ' + str( new_mu ) )
    logging.debug( 'Leaving the new_angle function' )
    sep()
    return( new_mu )

#This function determines in which spatial bin an interaction occurs
def location( place , bin_width , cep , sep ):
    '''This function determines in which bin an interaction occurs'''
    sep()
    logging.debug( 'Entering the location function' )
    cell = int( math.floor( place / float( bin_width ) ) )
    logging.debug( 'Cell is: ' + str( cell ) )
    logging.debug( 'Leaving the location function' )
    sep()
    return( cell )
        
#This function will determine if the neutron leaked
def leakage( location , leak_array , present , cep , sep ):
    '''This function tracks leakage'''
    sep()
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
    sep()
    return( present )

#This function determines the collision type
def col_type( csx_array , cep , sep ):
    '''Ths function determines the collision type'''
#Random number between 0 and 1
    sep()
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
    sep()
    return( col_type )

#This function generates a start position for our neutron
def start_pos( cep , sep ):
    '''This function generates a start pos for our neutron'''
    sep()
    logging.debug( 'Entering the start_pos function' )
    pos = np.random.random( 1 ) * 4.0
    cep()
    logging.debug( 'The starting position is ' + str( pos ) )
    logging.debug( 'Leaving the start_pos function' )
    sep()
    return( pos )

#This function generates a random angle on (-1,1)
def angle( cep , sep ):
    '''This function generates a random angle on (-1,1)'''
    sep()
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
    sep()
    return( ang )

#This function will give us the distance our neutron travels
def distance( t_sig , cep , sep ):
    '''This function calculates distance to next collision'''
    sep()
    logging.debug( 'Entering the distance function' )
    dis = -np.log( np.random.random( 1 ) ) / t_sig
    logging.debug( 'The calculated distance is ' + str( dis ) )
    logging.debug( 'Leaving the distance function' )
    sep()
    return( dis )

#This function will calculate the flux distribution based
#   on the collision flux estimator
def flux_collision( col_array , abs_array , num_part , cell_width, \
                        num_bins , xs_array, cep , sep ):
    '''This function will calculate the collision estimated flux 
        as well as its error and write these to csv files '''
    sep()
    logging.debug( 'Entering the flux_collision function' )
#Define total interaction array
    interactions = col_array + abs_array
#Initialize the phi array
    phi = np.zeros( ( 1 , num_bins ) )
#Calculate collision flux
    phi[ 0 ] = ( interactions ) / ( xs_array[ 0 ] * \
        float( cell_width ) * float( num_part ) )
#Store non-normalized flux
    nn_phi = phi[ 0 ]
#Normalize collision flux
    phi[ 0 ] = phi[ 0 ] / sum( phi[ 0 ] )
#Calculate estimated mean
    est_mean = ( interactions ) / float( num_part )
#Calculate phi error
    phi[ 1 ] = np.sqrt( ( np.square( interactions - est_mean ) / \
        ( float( num_part - 1 ) ) ) / ( xs_array[ 0 ] * \
            float( cell_width ) * float( num_part ) ) )
#Store error associated with the sum of the nn_phi array
    sum_error = math.sqrt( sum( np.square( phi[ 1 ] ) ) )
#Calculate the normalized flux error
    phi[ 1 ] = np.sqrt( ( np.square( phi[ 1 ] ) / sum( nn_phi ) ) \
        + ( np.square( nn_phi ) / ( sum( nn_phi )**2 ) ) * \
        sum_error )
    logging.debug( 'Leaving the flux_collision function' )
    sep()
    return( phi ) 

#This function will calculate the abs rate in slab halves        
def abs_half_cells( abs_array , cep , sep ):
   '''This function calculates abs rates and probabilities in
      half-cells'''
   sep()
   logging.debug( 'Entering the abs_half_cell function' )
#Array index of right end of left half of cell
   h_index = len( abs_array ) / 2 - 1
   logging.debug( 'Index of right end of left cell:' \
    + str( h_index ) )
#Initilize the array
   abs_report = np.zeros( ( 1 , 1 ) )
   total_abs = float( sum( abs_array ) )
   abs_report[ 0 , 0 ] = total_abs - sum( abs_array , \
    h_index + 1 )
   abs_report[ 0 , 1 ] = sum( abs_array , h_index + 1 )
   logging.debug( 'Absorption half cell array: ' )
   logging.debug( str( abs_report[ 0 ] ) )
   logging.debug( 'Total absorption is: ' + \
       str( total_abs ) )
   abs_report[ 1 ] = abs_report[ 0 ] / total_abs
   logging.debug( 'Abs probability half cell array:' )
   logging.debug( str( abs_report[ 1 ] ) )
   logging.debug( 'Leaving the abs_half_cell function' )
   sep()
   return( abs_report )

#This function will calculate our leakage prob
def currents( l_array , num_part ):
    '''This function will produce leakage prob'''
    sep()
    logging.debug( 'Entering the currents function' )
#Generate leakage probabilities
    cur_report = l_array / float( num_part )
    logging.debug( 'Leaving the currents function' )
    sep()
    return( cur_report )
	
#This function will plot our flux
def plotter( flux , num_part , num_bins , width , cep , sep ):
    '''This function will plot our flux'''
    sep()
    logging.debug( 'Entering plotting function' )
    bins = [ x * width for x in range( num_bins ) ]
    phi = [ x for pair in zip( flux[ 0 ] , flux[ 0 ] ) for x in pair ]
    label_string = 'N = ' + str( num_part )
    save_string = 'P3Plot' + str( num_part )
    plot( bins , phi , label = label_string )
    xlabel( 'Position in cm' )
    ylabel( 'Normalized Flux (#/s*cm*cm)' )
    title( 'Scalar Flux Distribution' )
    savefig( save_string )
    logging.debug( 'Leaving the plotting function' )
    sep()
    return 

#Lets begin our neutron histories loop
for i in range( N ):
     Lifetime( collisions , absorptions , leak_array , sig_array , \
                    cell_length , start_pos , angle , \
                    distance , leakage , collide , col_type , \
                    location , new_angle , cep , sep )
#Now we generate the flux
Phi = flux_collision( collisions , absorptions , N , cell_length, \
                        h , sig_array, cep , sep )

#Now we plot the flux
plotter( Phi , N , h , cell_length , cep , sep )

#Now we generate the absorption information
abs_out = abs_half_cells( absorptions , cep , sep )

#Now we generate our leakage probabilities
leak_prob = currents( leak_array , N )

#We also print to the log file

sep()
logging.debug( 'The number of particles used is: ' + str( N ) )
cep()
logging.debug( 'The abs rate is: ' + str( abs_out[ 0 ] ) )
logging.debug( 'The abs prob is: ' + str( abs_out[ 1 ] ) )
cep()
logging.debug( 'The leakage rate is: ' + str( leak_array ) )
logging.debug( 'The leak prob is: ' + str( leak_prob ) )

# Let the user know it has all ended
print "Sn CODE END!!"
print "*************************************************************"
