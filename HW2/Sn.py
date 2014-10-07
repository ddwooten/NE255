#!/usr/bin/python
# Creator: Daniel Wooten
# NE255 HW2 Sn Code

import csv as csvreader
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

print "*****************************************************"
print "Sn CODE BEGIN!"
print "Reading input file"

# This is the csv file from which we will read in cross sx,
# etc and other code options. In place of user input
csvfile = open( 'input3.csv' , 'r' )
reader = csvreader.reader( csvfile )

# Initilizing the array to hold the inputs
csvinput = []

# This will create an array of stirngs from the csv file and convert them to
# floats
r_index = 0
for row in reader:
	csvinput.append( row )
	for column in range( len(csvinput[ r_index ] ) ):
		if len( csvinput[ r_index ][ column ] ) != 0:
			csvinput[ r_index ][ column ] = float( 
				csvinput[ r_index ][ column ] )
	r_index += 1

LogFileName = 'logfile.dat'

OutputFile = 'output.dat'

# These are the row indicies where the various parameters are
# stored
MuRow = 1
Sig0Row = 2
Sig1Row = 3
SrcRow = 4
BCLRow = 5
BCRRow = 6
SigTRow = 7
QRow = 8
JRow = 9
DimRow = 10

# This exits if no log level was set or set improperly
try:
	LogLevel = int( csvinput[ 0 ][ 0 ] )
except:
	sys.exit( "ERROR!!: Log level can not be cast as an integer" )

#This does some basic config on the log file
logging.basicConfig( filename = LogFileName , format = "[%(levelname)8s] %(message)s" \
    , filemode = 'w' , level = LogLevel )
logging.debug( "This is the debug level reporting in" )
logging.info( "This is the info level reporting in " )
logging.warning( "This is the warning level reporting in" )
logging.error( "This is the error level reporting in" )
logging.critical( "This is the critical level reporting in" )

#Here we define some quadrature arrays
Mu2 = [-0.577350269189626,0.577350269189626]
W2 = [1,1]
Mu4 = [-0.861136311594053,-0.339981043584856,0.339981043584856,
	0.861136311594053]
W4 = [0.347854845137454,0.652145154862546,0.652145154862546
	,0.347854845137454]
Mu8 = [-0.962089856497536,-0.796666477413627,-0.525532409916329,
	-0.183434642495650,0.183434642495650,0.525532409916329
	,0.796666477413627,0.962089856497536]
W8 = [0.101228536290376,0.22238103445337,0.313706645877887,
	0.362683783378363,0.362683783378363,0.313706645877887,
	0.22238103445337,0.101228536290376]
Mu16 = [-0.989400934991650,-0.94457023073233,-0.865631202387832,
	-0.755404408355003,-0.617876244402644,-0.458016777657227,
	-0.281603550779259,-0.095012509837637,0.095012509837637
	,0.281603550779259,0.458016777657227,0.617876244402644
	,0.755404408355003,0.865631202387832,0.94457023073233
	,0.989400934991650]
W16 = [0.027152459411754,0.062253523938648,0.095158511682493,
	0.124628971255534,0.149595988816577,0.161956519395003,
	0.182603415044924,0.189450610455067,0.189450610455067
	,0.182603415044924,0.161956519395003,0.149595988816577
	,0.124628971255534,0.095158511682493,0.062253523938648
	,0.027152459411754]

# From the input file we know which Sn method we desire
# We use this input parameter 
Q_set = csvinput[ QRow ][ 0 ]

if Q_set == 2:
	mu_array = Mu2
	w_array = W2
elif Q_set == 4:
	mu_array = Mu4
	w_array = W4
elif Q_set == 8:
	mu_array = Mu8
	w_array = W8
elif Q_set == 16:
	mu_array = Mu16
	w_array = W16
else:
	sys.exit( "ERROR!!: Qudrature, row" + str( QRow ) + " , not set or \
	invalid" )
cep()
logging.debug( "The quadrature set chosen is Sn " +str( Q_set ) )
logging.debug( "The selected mu array is" )
logging.debug( str( mu_array ) )
logging.debug( "The corresponding weights array is " )
logging.debug( str( w_array ) )
cep()

# Here we define some short hand for various arrays we will need
src = csvinput[ SrcRow ]
cep()
logging.debug( "The source array is given as " )
logging.debug( str( src ) )
Sig0 = csvinput[ Sig0Row ]
cep()
logging.debug( "The sigma 0 scattering array is given as " )
logging.debug( str( Sig0 ) )
Sig1 = csvinput[ Sig1Row ]
cep()
logging.debug( "The sigma 1 scattering array is given as " )
logging.debug( str( Sig1 ) )
BconL = csvinput[ BCLRow ]
cep()
logging.debug( "The left boundary condition array is given as " )
logging.debug( str( BconL ) )
BconR = csvinput[ BCRRow ]
cep()
logging.debug( "The right boundary condition array is given as " )
logging.debug( str( BconR ) )
SigT = csvinput[ SigTRow ]
cep()
logging.debug( "The sigma total array is given as " )
logging.debug(str(SigT))
h_Value = csvinput[ DimRow ][ 0 ] 
cep()
logging.debug( "The width of each cell is given as " + str( h_Value ) )
num_Cell = int( csvinput[ JRow ][ 0 ] ) 
cep()
logging.debug( "The number of cells is given as " + str( num_Cell ) )
num_Quad = int( csvinput[ QRow ][ 0 ] )
cep()
logging.debug( "The number of quadrature is given as " + str( num_Quad ) )


def Build_Matrix( J , N , source , S0 , S1 , St, BCL , BCR , h, mu, w, cep ):
	''' This function builds our coefficients matrix to solve
		the given problem '''
	cep()
	logging.debug( "Begining the Build_Matrix routine" )
	mat = np.zeros( ( ( J + 1 ) * N , ( J + 1 ) * N ) )
	for j in range( J ):
		cep()
		logging.debug( " Working on the " + str( j ) + " cell" )
		for n in range( N ):
			mat[ ( N * j + n ) , ( N * j + n ) ] = ( -mu[ n ] / h )	+ ( St[ j ] / 2.0 )  
			logging.debug( "The " + str( N * j + n ) + " row ( " + str( j ) + \
				" edge ) and the " + str( N * j + n ) + " column ( " \
				+ str( n ) + " direction ) have value " \
				+ str( mat[ N * j + n , N * j + n ] ) )
			if j + 1 < J:
				mat[ N * j + n, N * ( j + 1 ) + n ] = ( mu[ n ] / h ) + \
					 ( St[ j + 1 ] / 2.0 )
				logging.debug( "The " + str( N * j + n ) + " row ( " + str( j + 1 ) + \
					" edge ) and the " + str( N * ( j + 1 ) + n ) + " column ( " \
					+ str( n ) + " direction ) have value " \
					+ str( mat[ N * j + n , N * ( j + 1 ) + n ] ) )
			logging.debug( "Populating the scattering terms for the " + str( j ) + \
				" cell and the " + str( n ) + " direction" )
			for nprime in range( N ):
				mat[ N * j + n , N * j + nprime ] = mat[ N * j + n , \
					N * j + nprime ] - ( w[ nprime ] * ( 1.0 / 2.0 ) ) \
				* ( S0[ j ] + 3.0 * mu[ n ] * mu[ nprime ] * S1[ j ] ) 
				logging.debug( "The " + str( N * j + n ) + " row ( " + str( j ) + \
				" edge ) and the " + str( N * j + nprime ) +  " column ( " + \
				str( nprime ) + " direction ) has value " + \
				str( mat[ N * j + n , N * j + nprime ] ) )
			logging.debug( "Done populating scattering terms for the " + str( j ) + \
				" cell and the " + str( n ) + " direction" )
		logging.debug( "Done with the " + str( j ) + " cell" )
	cep()
	logging.debug( "Applying boundary conditions" )
# This is the number of left/right boundary equations that we have
	n_boundary = int( N / 2 )
	for n in range( n_boundary ):
		cep()
		mat[ N * J + ( 2 * n ) , ( N - n ) ] = 1
		logging.debug( "The " + str( N * J + ( 1 + 2 * n ) ) + " row ( left BC ) for \
		the " + str( N - n ) + " direction has value 1" )
		mat[ N * J + ( 1 + 2 * n ) , N * J + n ] = 1	
		logging.debug( "The " + str( N * J + ( 2 + 2 * n ) ) + " row ( right BC ) for \
		the " + str( n ) + " direction has value 1" )
	logging.debug( "End apply boundary conditions" )
	logging.debug( "Exiting the Build_Matrix routine" )
	cep()
	return( mat )

cep()
logging.debug( "Calling the Build_Matrix routine" )
matrix = Build_Matrix( num_Cell , num_Quad , src , Sig0 , Sig1 , SigT , BconL \
	, BconR , h_Value , mu_array , w_array , cep )
cep()
logging.debug( "The constructed matrix has form" )
if LogLevel <= 10:
	for row in range( ( num_Cell + 1 ) * num_Quad ):
		outstring = ''
		for col in range( (num_Cell + 1) * num_Quad ):
			outstring = outstring + str( matrix[ row , col ] )[0:3] + ' '
		logging.debug( outstring )
logging.debug( "End of file" )
print "Sn CODE END!!"
print "*************************************************************"
