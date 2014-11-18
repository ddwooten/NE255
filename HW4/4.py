#!/usr/bin/python
# Creator: Daniel Wooten
# NE255 HW4 P3 MC Code

import logging as logging
import time as time
import sys as sys
import numpy as np
import math as math
import pylab as pl
import csv as csvreader
import mpmath as mp

#This sets the precision for mpmath (extended precision python)
mp.dis = 70

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
print "Photon CODE BEGIN!"

#Take in the number of samples
N = int( raw_input('Please input the number of samples\n') )

#Here we will intake data for the photon cross sections
csvfile = open( 'raw_xs.txt' , 'r' )
reader = csvreader.reader( csvfile )
array = []
for row in reader:
    array.append( row )
att_array = np.zeros( ( len( array ) , 3 ) )
for row in range( len( array ) ):
    for column in range( len( array[ row ] ) ):
        att_array[ row ][ column ] = float( array[ row ][ column ] )

#Define the number of spatial bins
h = 10


#Define cell length
cell_length = 5.0 / float( h )

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

if LogLevel <= 10:
    sep()
    logging.debug( 'The cross sections array is: ' )
    cep()
    for row in range( len( att_array ) ):
        logging.debug( str( att_array[ row ] ) )

#This function will follow the lifespan of one neutron
def Lifetime( col_counter , abs_counter , leak_counter , xs , \
                cell_width , start_pos , angle , \
                distance , leakage , collide , col_type , \
                location , new_angle , xs_data , cep , sep ):
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
#Start the neutron off with a position and an angle and energy
    pos = start_pos( cep , sep )
    cep()
    logging.debug( 'Neutron is starting at: ' + str( pos ) )
    mu = angle( cep , sep )
    cep()
    logging.debug( 'Neutron has angle: ' + str( mu ) )
    eng = 0.05
    cep()
    logging.debug( 'Neutron has energy: ' + str( eng ) )
#Counter for number of loops
    num_col = 0
#Initilize the count variable
    count = 0
#Here we begin the tracking loop
#While the neutron is both not absorbed and not leaked
    while ( inside and alive ):
        cep()
        logging.debug( 'Tracking collision number: ' + str( num_col ) )
#Determine the photon cross sections
        xs_array = xs( xs_data , eng , cep , sep )
#Get the total distance traveled
        dis = distance( xs_array[ 0 ] ,  cep , sep )
        cep()
        logging.debug( 'Neutron is traveling distance: ' + \
            str( dis ) )
        cep()
        logging.debug( 'Projected distance is: ' + str( dis * mu ) )
#Project onto the x axis
        old_pos = pos
        pos = pos + dis * mu
        cep()
        logging.debug( 'New position is: ' + str( pos ) )
#Check for scoring albedo
        logging.debug( 'num_col is: ' + str( num_col ) )
        if num_col > 0 and num_col < 2:
            logging.debug( 'Tripped' )
            count = score( mu , pos , eng , \
                 count, old_pos ,  cep , sep )
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
        logging.debug( 'Incoming energy is: ' + str( eng ) )
        if alive and inside: res = collide( pos , mu , col_counter, \
           abs_counter , \
           alive, angle , col_type , location , xs_array , cell_width\
           , new_angle , eng , cep , sep )
           alive = res[ 0 ]
           mu = res[ 1 ]
        cep()
        logging.debug( 'Neutron parameters post collision: ' )
        logging.debug( 'Outgoing angle is: ' + str( mu ) )
        cep()
        logging.debug( 'Neutron is alive: ' + str( alive ) )
        logging.debug( 'Neutron is inside: ' + str( inside ) )
#Increment the collision number
        logging.debug( 'Tripped, incrementing num_col')
        num_col += 1
        logging.debug( str( num_col ) )
    cep()
    logging.debug( 'Albedo for this photon is: ' + str( count ) )
    logging.debug( 'Terminating neutron history' )
    sep()
    return( count )

#This function will score our albedo
def score(  angle , place , energy , alb , old_place , cep , sep ):
    '''This function will score our albedo'''
    sep()
    logging.debug( 'Entering the score function' )
#Set default value
    mark = 0
    if angle < 0 and place >= abs( old_place / angle ):
       mark = energy * angle
    cep()
    logging.debug( 'mark has value: ' + str( mark ) )
    cep()
    logging.debug( 'Leaving the score function' )
    sep()
    return( mark )

#This function will determine photon cross sections
def xs( data , energy , cep , sep ):
    '''This function will determine photon cross sections'''
    sep()
    logging.debug( 'Entering the xs function' )
#Init the storage array
    cs_array = np.zeros( 3 )
#Here we define the concreate density
    rho = 2.3
#Here we define a rough electron density
    e_den = mp.mpf( 3 * 10**( 23 ) * 100**3 )
#Here we define the speed of light, planks const, and electron mass
    plank = mp.mpf( 6.626 * 10**( -34 ) )
    qo = mp.mpf( 1.602 * 10**( -19 ) )
    light = mp.mpf( 3.0 * 10**( 8 ) )
    mass = mp.mpf( 9.109 * 10**( -31 ) )
#Set the energy as an extended precision number
    eng = mp.mpmathify( energy )
    eng = eng * 10**( -13 )
#Get the frequency
    v = eng / plank
#This is a fudge factor to get the compton xs to be close to realistic
    f = 10**(31)
#Here we calculate the compton cross section
    radius = qo**4 / ( mass * light**2 )
    alpha = ( eng ) / ( mass * light**2 )
    cs_xs = 2 * mp.pi * radius * ( ( ( 1.0 + alpha ) \
        / ( alpha**2 ) ) * ( ( ( 2.0 * ( 1.0 + alpha ) \
        ) / ( 1.0 + 2.0 * alpha ) ) - ( 1.0 / alpha ) * \
        ( mp.log( 1.0 + 2.0 * alpha ) ) ) + ( ( 1.0 / \
        ( 2.0 * alpha ) ) * mp.log( 1.0 + 2.0 * alpha ) - \
        ( ( 1.0 + 3.0 * alpha ) / ( 1.0 + 2.0 * alpha )**2 ) ) )
    cep()
    logging.debug( 'The micro cs xs is: ' + mp.nstr( \
        cs_xs , n = 10 ) )
    mu_cs = cs_xs * e_den * f
    logging.debug( 'The macro cs xs is: ' + mp.nstr( \
        mu_cs , n = 10 ) )
    cs_array[ 1 ] = float( mp.nstr( mu_cs , n = 10 ) )
#Now we will determine, via linear interp, the total xs
    cep()
    logging.debug( 'Energy of photon is: ' + str( energy ) )
    if energy <= data[ 0 , 0 ]:
        logging.debug( 'Lowest energy point is: ' + \
            str( data[ 0 , 0 ] ) )
        logging.debug( 'Xs at lowest energy is: ' + \
            str( data[ 0 , 1 ] ) )
        cs_array[ 0 ] = ( ( data[ 1 , 1 ] - data[ 0 , 1 ] ) \
            ( data[ 1 , 0 ] - data[ 0 , 0 ] ) ) * ( \
            data[ 0 , 0 ] - energy ) - data[ 0 , 1 ]
        logging.debug( 'Calculated XS is: ' + \
            str( cs_array[ 0 ] ) )
    else:
        for row in range( len( data ) - 1 ):
            index = row + 1
            if energy <= data[ index , 0 ]:
                logging.debug( 'Energy of photon is: '\
                     + str( energy ) )
                logging.debug( 'Energy of lower XS is: ' \
                    + str( data[ index - 1 , 0 ] ) )
                logging.debug( 'Energy of higher XS is: ' \
                    + str( data[ index , 0 ] ) )
                logging.debug( 'Lower XS is: ' + \
                    str( data[ index -1 , 1 ] ) )
                logging.debug( 'Higher XS is: ' +
                    str( data[ index , 1 ] ) )
                cs_array[ 0 ] = ( ( data[ index , 0 ] - \
                    data[ index - 1 , 0 ] ) / ( \
                    data[ index , 1 ] - data[ index - 1 , 1 ] \
                    ) ) * ( data[ index , 0 ] - energy ) + \
                    data[ index -1 , 1 ]
                logging.debug( 'Calculated XS is: ' + \
                   str( cs_array[ 0 ] ) )
                break
#Multiply by rho
    cs_array[ 0 ] = cs_array[ 0 ] * rho
    cs_array[ 2 ] = cs_array[ 0 ] - cs_array[ 1 ]
    cep()
    logging.debug( 'The cs_array is: ' + str( cs_array ) )
    logging.debug( 'Leaving the xs function' )
    sep()
    return( cs_array )

#This function will handle colliding neutrons
def collide( position , MU , col , absor , existance , angle \
                , col_type , location , cs , width , new_angle \
                , energy , cep , sep ):
    '''This function collides neutrons and hanldes the aftermath'''
    sep()
    logging.debug( 'Entering the colision routine' )
#holder array
    holder = [ True , 0.0 ]
#Determine the type of collision
    collision = col_type( cs , cep , sep )
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
        logging.debug( 'Incoming energy is: ' +str( energy ) )
        out = compton( MU , energy , cep , sep )
        MU = out[ 0 ]
        holder[ 1 ] = MU
        energy = out[ 1 ] 
        cep()
        logging.debug( 'Outgoing angle: ' + str( MU ) ) 
        logging.debug( 'Outgoing energy is: ' + str( energy ) )
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
        holder[ 0 ] = False  
        cep()
        logging.debug( 'Neutron is now alive: ' + str( existance ) )
    logging.debug( 'Leaving the collision function' )
    sep()
    return( holder )

#This function calculates an outgoing angle post scattering
def new_angle( incoming , x_sec , energy , cep , sep ):
    '''This function calculates an outgoing compton angle and energy'''
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

#This function will sample the photon energy in compton scattering
def compton( old_angle , energy , cep , sep ):
    '''This function samples the compton scattering energy for a photon'''
    sep()
    logging.debug( 'Entering the compton function' )
#Init our out array
    out = np.zeros( 2 )
#Define some constants
    #plank = mpf( 6.626 * 10**( -34 ) )
    #light = mpf( 3.0 * 10**( 8 ) )
    #mass = mpf( 9.109 * 10**( -31 ) )
#Get our lambda ( may need adjusting )
    #lam = ( mass * light**2 ) / ( energy / plank )
    lam = 0.511 / energy
    #logging.debug( 'Lambda is: ' + mp.nstr( lam , n = 10 ) )
    logging.debug( 'Lambda is: ' + str( lam ) )
    #lam = float( mp.nstr( lam , n = 10 ) )
#Enter the x selection algorithm
    while out[ 1 ] == 0 :
#Generate our three random numbers
        nums = np.random.random( 3 )
        if nums[ 0 ] <= ( ( lam + 2.0 ) / ( 9.0 * lam + 2.0 ) ):
            x1 = 1.0 + 2.0 * nums[ 1 ] / lam
            if nums[ 2 ] <= 4.0 * ( 1.0 / x1 - 1.0 / x1**2 ):
                out[ 1 ] = 0.511 / ( x1 * lam )
        else:
            x1 = ( lam + 2.0 ) / ( lam + 2.0 * nums[ 1 ] )
            if nums[ 2 ] <= 0.5 * ( ( lam - lam * x1 + 1.0 )**2 \
               + 1.0 / x1 ):
               out[ 1 ] = 0.511 / ( x1 * lam ) 
    cep()
    logging.debug( 'Old energy: ' + str( energy ) )
    logging.debug( 'New energy: ' + str( out[ 1 ] ) )
#Generate and store outgoing angle
    out[ 0 ] = math.cos( math.acos( old_angle ) + \
        math.acos( 1.0 - lam * ( x1 - 1.0 ) ) )
    logging.debug( 'Old angle: ' + str( old_angle ) )
    logging.debug( 'New angle: ' + str( out[ 0 ] ) )
    logging.debug( 'Leaving the compton function' )
    sep()
    return( out )

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
    if location > 5.0: present = False ; leak_array[ 1 ] += 1
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
        str( csx_array[ 2 ] / csx_array[ 0 ] ) )
    cep()
    if quanta <= csx_array[ 2 ] / csx_array[ 0 ]:
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
    pos = 0.0
    cep()
    logging.debug( 'The starting position is ' + str( pos ) )
    logging.debug( 'Leaving the start_pos function' )
    sep()
    return( pos )

#This function generates a random angle on (-1,1)
def angle( cep , sep ):
    '''This function doesn't do much for photons'''
    sep()
    logging.debug( 'Entering the angle function' )
    ang = 1.0
    logging.debug( 'Leaving the angle function' )
    sep()
    return( ang )

#This function will give us the distance our neutron travels
def distance( xs , cep , sep ):
    '''This function calculates distance to next collision'''
    sep()
    logging.debug( 'Entering the distance function' )
    dis = -np.log( np.random.random( 1 ) ) / xs 
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
    cep()
    logging.debug( 'Interactions array: ' )
    interactions = col_array + abs_array
    logging.debug( str( interactions ) )
#Initialize the phi array
    phi = np.zeros( ( 2 , num_bins ) )
#Calculate collision flux
    cep()
    logging.debug( 'First phi array: ' )
    phi[ 0 ] = ( interactions ) / ( xs_array[ 0 ] * \
        float( cell_width ) * float( num_part ) )
    logging.debug( str( phi[ 0 ] ) )
#Store non-normalized flux
    nn_phi = phi[ 0 ]
#Normalize collision flux
    cep()
    logging.debug( 'Normalized phi array' )
    phi[ 0 ] = phi[ 0 ] / sum( phi[ 0 ] )
    logging.debug( str( phi[ 0 ] ) )
#Calculate estimated mean
    cep()
    logging.debug( 'est mean array: ' )
    est_mean = ( interactions ) / float( num_part )
    logging.debug( str( est_mean ) )
#We pull sig_t out of the array (causing problems with np)
    Tsig = xs_array[ 0 ]
    cep()
    logging.debug( 'Tsig: ' + str( Tsig ) )
#Calculate phi error
    phi[ 1 ] = np.sqrt( ( np.square( interactions - est_mean ) ) / \
        ( float( num_part - 1 ) * float( num_part ) \
         * ( float ( Tsig ) * float( cell_width ) * float( num_part ) ) ) )
    cep()
    logging.debug( str( ( float( num_part - 1 ) * float( num_part ) \
         * ( float ( Tsig ) * float( cell_width ) * float( num_part ) ) ) ) )
    logging.debug( 'First phi error array: ' )
    logging.debug( str( phi[ 1 ] ) )
#Store error associated with the sum of the nn_phi array
    sum_error = math.sqrt( sum( np.square( phi[ 1 ] ) ) )
#Calculate the normalized flux error
    phi[ 1 ] = np.sqrt( ( np.square( phi[ 1 ] ) / np.square( sum( nn_phi ) ) ) \
        + ( np.square( nn_phi ) / ( sum( nn_phi )**2 ) ) * \
        sum_error**2 )
    cep()
    logging.debug( 'Normalized phi error array: ' )
    logging.debug( str( phi[ 1 ] ) )
    cep()
    logging.debug( 'Leaving the flux_collision function' )
    sep()
    return( phi ) 

#This function will calculate the abs rate in slab halves        
def abs_half_cells( abs_array , num_part , cep , sep ):
   '''This function calculates abs rates and probabilities in
      half-cells'''
   sep()
   logging.debug( 'Entering the abs_half_cell function' )
#Array index of right end of left half of cell
   h_index = len( abs_array ) / 2 - 1
   logging.debug( 'Index of right end of left cell:' \
    + str( h_index ) )
#Initilize the array
   abs_report = np.zeros( ( 4 , 2 ) )
#Get total absoprtions
   total_abs = float( sum( abs_array ) )
#Get abs, per cell, estimated mean
   abs_m = abs_array / float( num_part )
#Get abs var
   abs_v = ( abs_array - abs_m )**2 / ( \
    float( num_part + 1 ) * float( num_part ) )
#Get abs s.error
   abs_e = np.sqrt( abs_v )
#Get error of left half sum
   abs_e_l = math.sqrt( sum( abs_v[ 0 : h_index ] ) )
#Get error of right half sum
   abs_e_r = math.sqrt( sum( abs_v[ h_index + 1 : ] ) )
#Get error of total sum
   abs_s_e = math.sqrt( sum( abs_v ) )
#Get abs rate in left half
   abs_report[ 0 , 0 ] = sum( abs_array[ 0 : h_index ] )
#Get abs rate in right half
   abs_report[ 0 , 1 ] = sum( abs_array , h_index + 1 )
   logging.debug( 'Absorption half cell array: ' )
   logging.debug( str( abs_report[ 0 ] ) )
   logging.debug( 'Total absorption is: ' + \
       str( total_abs ) )
#Store error
   abs_report[ 1 , 0 ] = abs_e_l
   abs_report[ 1 , 1 ] = abs_e_r
#Get abs prob
   abs_report[ 2 ] = abs_report[ 0 ] / float( num_part )
   logging.debug( 'Abs probability half cell array:' )
   logging.debug( str( abs_report[ 1 ] ) )
#Store error for prob
   abs_report[ 3 ] = abs_report[ 1 ] / float( num_part )
   logging.debug( 'Leaving the abs_half_cell function' )
   sep()
   return( abs_report )

#This function will calculate our leakage prob
def currents( l_array , num_part ):
    '''This function will produce leakage prob'''
    sep()
    logging.debug( 'Entering the currents function' )
#Init array
    cur_report = np.zeros( ( 3 , 2 ) )
#Calc leak error
    cur_report[ 0 ] = np.sqrt( np.square( l_array - l_array / \
        float( num_part ) ) / ( float( num_part - 1 ) ) )
#Generate leakage probabilities
    cur_report[ 1 , 0 ] = l_array[ 0 ] / float( num_part )
    cur_report[ 1 , 1 ] = l_array[ 1 ] / float( num_part )
#Gen leak prob error
    cur_report[ 2 ] = cur_report[ 0 ] / float( num_part )
    logging.debug( 'Leaving the currents function' )
    sep()
    return( cur_report )
	
#This function will plot our flux
def plotter( flux , num_part , num_bins , width , cep , sep ):
    '''This function will plot our flux'''
    sep()
    logging.debug( 'Entering plotting function' )
    logging.debug( 'First bins' )
    points = [ x * width for x in range( num_bins + 1 ) ]
    logging.debug( str( points ) )
    cep()
    logging.debug( 'Second bins' )
    bins = [ x for pair in zip( points , points ) for x in pair][1:-1]
    logging.debug( str( bins ) )
    mid_points = points[ 0 : len( points ) - 1 ] 
    mid_points = [ x + ( width / 2.0 ) for x in mid_points ]
    cep()
    logging.debug( 'mid_points array: ' )
    logging.debug( str( mid_points ) )
    cep()
    logging.debug( 'Phi' )
    cep()
    phi = [ x for pair in zip( flux[ 0 ] , flux[ 0 ] ) for x in pair ]
    phi_err = flux[ 1 ]
    logging.debug( str( phi ) )
    logging.debug( str( len( mid_points ) ) )
    logging.debug( str( len( phi_err ) ) )
    label_string = 'N = ' + str( num_part )
    save_string = 'P3Plot' + str( num_part )
    pl.plot( bins , phi , 'b-' , label = label_string )
    pl.plot( mid_points , flux[ 0 ] , marker = '.' , color = 'b' , \
         visible = False )
    pl.errorbar( mid_points , flux[ 0 ] , yerr = phi_err , linestyle = 'None' )
    pl.xlabel( 'Position in cm' )
    pl.ylabel( 'Normalized Flux (#/s*cm*cm)' )
    pl.title( 'Scalar Flux Distribution' )
    pl.savefig( save_string )
    logging.debug( 'Leaving the plotting function' )
    sep()
    return 

#Lets begin our neutron histories loop
albedo = 0
for i in range( N ):
     albedo += Lifetime( collisions , absorptions , leak_array , xs , \
                    cell_length , start_pos , angle , \
                    distance , leakage , collide , col_type , \
                    location , new_angle , att_array , cep , sep )

#Now we generate the flux
#Phi = flux_collision( collisions , absorptions , N , cell_length, \
#                        h , sig_array, cep , sep )

#Now we plot the flux
#plotter( Phi , N , h , cell_length , cep , sep )

#Now we generate the absorption information
abs_out = abs_half_cells( absorptions , N , cep , sep )

#Now we generate our leakage probabilities
leak_prob = currents( leak_array , N )

#We also print to the log file

sep()
logging.critical( 'The number of particles used is: ' + str( N ) )
cep()
logging.critical( 'The abs rate is: ' + str( abs_out[ 0 ] ) )
logging.critical( 'The abs rate error is: ' + str( abs_out[ 1 ] ) )
logging.critical( 'The abs prob is: ' + str( abs_out[ 2 ] ) )
logging.critical( 'The abs prob error is: ' + str( abs_out[ 3 ] ) )
cep()
logging.critical( 'The leakage rate is: ' + str( leak_array ) )
logging.critical( 'The error in leak rate is: ' + str( leak_prob[ 0 ] ) )
logging.critical( 'The leak prob is: ' + str( leak_prob[ 1 ] ) )
logging.critical( 'The leak prob error is: ' + str( leak_prob[ 2 ] ) )
cep()
logging.critical( 'The albedo number is: ' + str( albedo ) )
logging.critical( 'The albedo ratio is: ' +str( albedo * 0.5  / float( N ) ) )
albedo_error = math.sqrt( ( albedo - ( albedo * 0.5 / float( N ) ) )**2 \
    / ( float( N - 1 ) ) )
logging.critical( 'The albedo ratio error is: ' + str( albedo_error ) )

# Let the user know it has all ended
print "Sn CODE END!!"
print "*************************************************************"
