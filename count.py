#! /usr/bin/python

import sys
from collections import defaultdict
import math

def emmission_param(e_count,u_count):
	

try:
	input = open(sys.argv[1],"r")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

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
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

input.seek(0,0)
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
try:
	in_count = open("gene_train.temp","r")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

e_count = defaultdict(int)
u_count = defaultdict(int)
b_count = defaultdict(int)
t_count = defaultdict(int)

line = in_count.readline()
while(line):
	if line != "\n":
		words = line.split()
		if words[1] == "WORDTAG":
			e_count[(words[3],words[2])] = int(words[0])
		elif words[1] == "1-GRAM":
			u_count[words[2]] = int(words[0])
		elif words[1] == "1-GRAM":
			b_count[(words[3],words[2])] = int(words[0])
		elif words[1] == "1-GRAM":
			t_count[(words[4],words[2],words[3])] = int(words[0])
		else:
			print("Error")
			exit(1)
		
	line = in_count.readline()


in_count.close()
input.close()