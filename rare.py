#! /usr/bin/python

import sys
from collections import defaultdict
import math


try:
	input = open(sys.argv[1],"r")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

#count(x)

count = defaultdict(int)
line = input.readline()
while(line):
	if line != "\n":
		#print (line)
		word = line.split()[0]
		if word in count:
			count[word] += 1
		else:
			count[word] = 1
	line = input.readline()

'''
for key in count:
	print (key,':',count[key])
'''
try:
	out = open("gene_train.temp","w")
except IOError:
	sys.stderr.write("ERROR: Cannot open output file %s.\n" % arg)
	sys.exit(1)

#rset file pointer to start of file
input.seek(0,0)

#replace words with count < 5 with "_RARE_"

line = input.readline()
while(line):
	if line != "\n":
		words = line.split()
		if count[words[0]] < 5:
			putline = "_RARE_ " + words[1] + "\n"
		else:
			putline = line
		out.write(putline)
	else:
		out.write("\n")
	
	line = input.readline()

out.close()
input.close()