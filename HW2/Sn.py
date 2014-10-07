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
# Let the user know that the code is running
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
# File names for the log and output files respectively
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

# This does some basic config on the log file
logging.basicConfig( filename = LogFileName , format = "[%(levelname)8s] %(message)s" \
    , filemode = 'w' , level = LogLevel )
logging.debug( "This is the debug level reporting in" )
logging.info( "This is the info level reporting in " )
logging.warning( "This is the warning level reporting in" )
logging.error( "This is the error level reporting in" )
logging.critical( "This is the critical level reporting in" )

#Here we define some quadrature arrays
# Both the angular values and the weights
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
# We use this input parameter and the following if
# statements to set our quadrature
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

# This simply print out helpful info to the log file
cep()
logging.debug( "The quadrature set chosen is Sn " +str( Q_set ) )
logging.debug( "The selected mu array is" )
logging.debug( str( mu_array ) )
logging.debug( "The corresponding weights array is " )
logging.debug( str( w_array ) )
cep()

# Here we define some short hand for various arrays we will need
# as well as print out their values to the log file
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

# This function generates the rhs of the system of equations to solve
def RHS_Column( J, N, source, BCL, BCR, cep ):
	''' This function generates the right hand side solutions column
		that must be multiplied with the inverse of the 
		coefficients matrix to get the solution matrix '''
	cep()	
	logging.debug( "Begining the RHS_Column routine" )
	rhs = np.zeros( ( ( J + 1 ) * N , 1 ) )
# We populate the rhs with the source terms from input
	for j in range( J ):
		for n in range( N ):
			rhs[ N * j + n , 0 ] = source[ j ] * ( 1.0 / 2.0 )
	cep()
	logging.debug( "RHS of primary equations written" )	
	cep()
	logging.debug( "Applying boundary conditions" )
# This is the number of left/right boundary equations that we have
	n_boundary = int( N / 2 )
# We apply the boundary conditions, reading them from the input
	for n in range( n_boundary ):
		rhs[ N * J + ( 2 * n ) , 0 ] = BCL[ n ]
		rhs[ N * J + ( 1 + 2 * n ) , 0 ] = BCR[ n_boundary - 1 - n ]
	logging.debug(" Done applying boundary conditions" )
	logging.debug(" Exiting the RHS_Column routine" )
	return( rhs )

# This function will compute our partial currents at the boundary
def Part_Cur( J , N , w , mu , psi , cep ):
	'''This function will compute the partial currents
		at the boundary '''
	cep()
	logging.debug( "Begining the Part_Cur routine" )
	part_cur = np.zeros( ( 1 , 2 ) )
	n_part = int( N / 2.0 )
	for n in range( n_part ):
		part_cur[ 0 , 1 ] = part_cur[ 0 , 1 ] + w[ n ] * mu[ n ] * psi[ n , 0 ]
		part_cur[ 0 , 2 ] = part_cur[ 0 , 2 ] + w[ N - 1 - n ] * mu[ N - 1 - n ] * \
			psi[ N * J + N - 1 - n , 0 ]
	logging.debug( "Exiting the Part_Cur routine" )
	return( part_cur )

#This function will compute our absorption rates in each slab half
def Abs_Slab( J , phi , St , cep ):
	'''This function calculates the absorption rate in each
		half of the cell'''
	cep()
	logging.debug( "Begining Abs_Slab routine" )
	half_slab = int( J / 2 )
	abs_rate = np.zeros( ( 1 , 2 ) )
	for j in range ( half_slab ):
		abs_rate[ 0 , 1 ] = abs_rate[ 0 , 1 ] + phi[ j ] * St[ j ]
		abs_rate[ 0 , 2 ] = abs_rate[ 0 , 2 ] + phi[ J - j ] * St[ J - j ]
	logging.debug( "Exiting the Abs_Slab routine" )
	return( abs_rate )

# This function will compute our cell averaged fluxes
def Gen_Phi( J , N , w , psi, cep ):
	''' This function properly weights and averages
		an array of edge psi values to get at
		the cell averaged fluxes '''
	cep()
	logging.debug( "Begining the Gen_Phi routine" )
	phi = np.zeros( ( J , 1 ) )
	i = 0
# Here we loop through our psi array and appropriately weight
# and average ( accorrding to diamond difference ) for phi
	for j in range( 0 , J , 2 ):
		for n in range( N ):
			phi[ i , 0 ] = phi[ i , 0 ] + ( w[ n ] * psi[ N * j + n , 0 ] + \
				w[ n ] * psi[ N * ( j + 1 ) + n , 0 ] ) / 2.0
		i = i + 1
	logging.debug( "Exiting the Gen_Phi routine" )
	return( phi )

# This function will compute our cell averaged currents
def Gen_Cur( J , N , mu , w , psi, cep ):
	''' This function, taking an array of psis,
		will produce the corresponding and
		weighted currents '''
	cep()
	logging.debug( "Begining the Gen_Cur routine" )
	cur = np.zeros( ( J , 1 ) )
	i = 0
	for j in range( 0 , J , 2 ):
		for n in range( N ):
			cur[ i , 0 ] = cur[ i , 0 ] + w[ n ] * mu[ n ] * ( psi[ N * j + n , 0 ] + \
				psi[ N * ( j + 1 ) + n , 0 ] ) / 2.0
		i = i + 1
	logging.debug( "Exiting the Gen_Cur routine" )
	return( cur )
				
# This function, taking in various problem parameters as arrays,
# Will construct the coefficient matrix that we will need
# to invert to solve a given problem.
# This method will work for both purely absorbing, isotropic
# scattering, or linearly anisotropic scatering problems
# All that needs to be done is the proper cross sections
# set

def Build_Matrix( J , N , source , S0 , S1 , St, BCL , BCR , h, mu, w, cep ):
	''' This function builds our coefficients matrix to solve
		the given problem '''
	cep()
	logging.debug( "Begining the Build_Matrix routine" )
	mat = np.zeros( ( ( J + 1 ) * N , ( J + 1 ) * N ) )
# Loop through the spatial cells
	for j in range( J ):
		cep()
		logging.debug( " Working on the " + str( j ) + " cell" )
# Loop through the quadrature
		for n in range( N ):
# Calculate the coefficient from the derivative term
# as well as the total cross section term
			mat[ ( N * j + n ) , ( N * j + n ) ] = ( -mu[ n ] / h )	+ ( St[ j ] / 2.0 )  
			logging.debug( "The " + str( N * j + n ) + " row ( " + str( j ) + \
				" edge ) and the " + str( N * j + n ) + " column ( " \
				+ str( n ) + " direction ) have value " \
				+ str( mat[ N * j + n , N * j + n ] ) )
# This if statement is no longer used. Rather than potentially
# compromize the code, it has been modified to always be true.
# In this way, we properlly fill out our matrix
			if j - 1 < J:
				mat[ N * j + n, N * ( j + 1 ) + n ] = ( mu[ n ] / h ) + \
					 ( St[ j ] / 2.0 )
				logging.debug( "The " + str( N * j + n ) + " row ( " + str( j + 1 ) + \
					" edge ) and the " + str( N * ( j + 1 ) + n ) + " column ( " \
					+ str( n ) + " direction ) have value " \
					+ str( mat[ N * j + n , N * ( j + 1 ) + n ] ) )
			logging.debug( "Populating the scattering terms for the " + str( j ) + \
				" cell and the " + str( n ) + " direction" )
# Calculate the coefficients for the right hand side scattering terms
			for nprime in range( N ):
				mat[ N * j + n , N * j + nprime ] = mat[ N * j + n , \
					N * j + nprime ] - ( w[ nprime ] * ( 1.0 / 4.0 ) ) \
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
# Calculate the boundary condition coefficients for each edge
# startign with the mu that is furthest from 0
		mat[ N * J + ( 2 * n ) , ( N - 1 - n ) ] = 1
		logging.debug( "The " + str( N * J + ( 1 + 2 * n ) ) + " row ( left BC ) for \
		the " + str( N - 1 - n ) + " direction has value 1" )
		mat[ N * J + ( 1 + 2 * n ) , N * J + n ] = 1	
		logging.debug( "The " + str( N * J + ( 2 + 2 * n ) ) + " row ( right BC ) for \
		the " + str( n ) + " direction has value 1" )
	logging.debug( "End apply boundary conditions" )
	logging.debug( "Exiting the Build_Matrix routine" )
	return( mat )

cep()
logging.debug( "Calling the Build_Matrix routine" )

# Here we build our coefficient matrix by calling the above function
coeff_matrix = Build_Matrix( num_Cell , num_Quad , src , Sig0 , Sig1 , SigT , BconL \
	, BconR , h_Value , mu_array , w_array , cep )
print str( np.linalg.det( coeff_matrix ) )
np.savetxt( "coeff_matrix.csv" , coeff_matrix , delimiter = "," )

cep()
logging.debug( "Calling the RHS_Column routine" )

# Here we build the rhs solution vector for our matrix problem
rhs_column = RHS_Column( num_Cell , num_Quad , src , BconL , BconR , cep )

np.savetxt( "rhs_column.csv" , rhs_column , delimiter = "," )

cep()
logging.debug( "Calling the numpy linalg solver")

# Here we call a linear algebra matrix solver, part of the numpy
# package in python, which is itself part of the scientific computing
# package in python

psi_array = np.linalg.solve( coeff_matrix , rhs_column )

cep()
logging.debug( "Calling the Gen_Phi routine" )

# Here we call a function to generate our cell averaged scalar fluxes
phi_array = Gen_Phi( num_Cell , num_Quad , w_array , psi_array , cep )

# Here we save the phi array as a csv so we can plot it
np.savetxt( "phi.csv" , phi_array , delimiter = "," )

cep()
logging.debug( "Calling the Gen_Cur routine" )

# Here we call a function to generate our cell averaged currents
cur_array = Gen_Cur( num_Cell , num_Quad , mu_array , w_array , psi_array , cep )

cep()
logging.debug( "Calling the Part_Cur routine" )

# Here we call a function to generate our partial currents at the boundaries
# with the left boundary as the first entry and the right boundary as the
# second
part_cur_array = Part_Cur( num_Cell , num_Quad , w_array , mu_array, psi_array , cep )

#Here we print out the partial currents array so we can know their value
print "The partial currents: "
print str( part_cur_array[ 0 , 1 ] ) + " : left"
print str( part_cur_array[ 0 , 2 ] ) + " : right"

cep()
logging.debug( "Calling the Abs_Slab routine" )

# Here we call a function to calculate the absorption rate in each half
# of the slab
abs_array = Abs_Slab( num_Cell , phi_array , SigT , cep )

#Here we print out the absorption rates so we can know them
print "The absorption rates"
print str( abs_array[ 0 , 1 ] ) + " : left"
print str( abs_array[ 0 , 2 ] ) + " : right"

cep()
logging.debug( "The rhs_column has form" )
cep()
if LogLevel <= 10:
	for row in rhs_column:
		logging.debug( str( rhs_column[ row ] ) )

cep()
logging.debug( "The psi vector has form" )
cep()
if LogLevel <= 10:
	for row in psi_array:
		logging.debug( str( psi_array[ row ] ) )

cep()
logging.debug( "The phi vector has form" )
cep()
if LogLevel <= 10:
	for row in phi_array:
		logging.debug( str( phi_array[ row ] ) )

cep()
logging.debug( "The cur vector has form" )
cep()
if LogLevel <= 10:
	for row in cur_array:
		logging.debug( str( cur_array[ row ] ) )
# Here we print out the matrix to file in a nicely formatted fashion as
# this helps with debugging
cep()
logging.debug( "The constructed matrix has form" )
if LogLevel <= 10:
	for row in range( ( num_Cell + 1 ) * num_Quad ):
		outstring = ''
		for col in range( (num_Cell + 1) * num_Quad ):
			outstring = outstring + str( matrix[ row , col ] )[0:3] + ' '
		logging.debug( outstring )
logging.debug( "End of file" )

# Let the user know it has all ended
print "Sn CODE END!!"
print "*************************************************************"
