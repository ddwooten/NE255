#!/usr/bin/python
# Creator: Daniel Wooten
# NE255 HW2 Sn Code

import csv as csvreader
import logging as logging
import time as time
import sys as sys
import numpy as np

print "*****************************************************"
print "Sn CODE BEGIN!"
print "Reading input file"

# This is the csv file from which we will read in cross sx,
# etc and other code options. In place of user input
csvfile = open( 'input.csv' , 'r' )
reader = csvreader.reader( csvfile )

# Initilizing the array to hold the inputs
csvinput = []

# This will create an array of stirngs from the csv file and convert them to
# floats
for row in reader:
	csvinput.append( row )
	for column in len( csvinput[ row ]
		csvinput[ row ][ column ] = float( csvinput[ row ][ column ] )

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
CCRow = 7
QRow = 8
JRow = 9
DimRow = 10

# This exits if no log level was set or set improperly
try:
	LogLevel = int( csvinput[ 0 ][ 0 ]
except:
	sys.exit( "ERROR!!: Log level can not be cast as an integer" )

#This does some basic config on the log file
logging.basicConfig( filename = LogFileName , format ="[%(levelname)8s] %(message)s" \
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
W4 = [-0.347854845137454,-0.652145154862546,0.652145154862546
	,0.347854845137454]
Mu8 = [-0.962089856497536,-0.796666477413627,-0.525532409916329,
	-0.183434642495650,0.183434642495650,0.525532409916329
	,0.796666477413627,0.962089856497536]
W8 = [

print "Sn CODE END!!"
print "*************************************************************"
