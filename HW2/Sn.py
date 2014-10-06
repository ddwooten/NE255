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

csvfile = open( 'input.csv' , 'r' )
reader = csvreader.reader( csvfile )

csvinput = []

LogFileName = 'logfile.dat'

OutputFile = 'output.dat'
