#! /usr/bin/python

import sys
from collections import defaultdict
import math

try:
	input = open(sys.argv[1],"r")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

count = {}
line = input.readline()
while(line):
	word = line.split()[0]
	if word in count:
		count[word] += 1
	else:
		count[word] = 1
	line = input.readline()


for key in count:
	print (key,':',count[key])