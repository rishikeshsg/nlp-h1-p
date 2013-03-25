#! /usr/bin/python

import sys
from collections import defaultdict
import math

def emmission_param(e_count,u_count,e_param,count):
	for key in u_count:
		for word in count:
			if (word,key) in e_count:
				e_param[(word,key)] = float(e_count[(word,key)])/u_count[key]
		if ("_RARE_",key) in e_count:
			e_param[("_RARE_",key)] = float(e_count[("_RARE_",key)])/u_count[key]

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
	in_count = open("gene.count","r")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

e_count = defaultdict(int)
u_count = defaultdict(int)
b_count = defaultdict(int)
t_count = defaultdict(int)

e_param = defaultdict(float)

line = in_count.readline()
while(line):
	if line != "\n":
		words = line.split()
		if words[1] == "WORDTAG":
			e_count[(words[3],words[2])] = int(words[0])
		elif words[1] == "1-GRAM":
			u_count[words[2]] = int(words[0])
		elif words[1] == "2-GRAM":
			b_count[(words[3],words[2])] = int(words[0])
		elif words[1] == "3-GRAM":
			t_count[(words[4],words[2],words[3])] = int(words[0])
		else:
			print("Error -->",words[1])
			exit(1)
		
	line = in_count.readline()

in_count.close()
input.close()

try:
	input = open("gene.dev","r")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

try:
	output = open("gene_dev.p1.out","w")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)


emmission_param(e_count,u_count,e_param,count)

line = input.readline()
while line:
	if line != "\n":
		test_word = line.split()
		max_e_count = -1.0
		tag = ""
		for key in u_count:
			if((test_word[0] in count) and (count[test_word[0]] >= 5)):
				if e_param[(test_word[0],key)] > max_e_count:
					max_e_count = e_param[(test_word[0],key)]
					tag = key
			else:
				if e_param[("_RARE_",key)] > max_e_count:
					max_e_count = e_param[("_RARE_",key)]
					tag = key
		output.write(test_word[0] + " " + tag + "\n")
	else:
		output.write("\n")
	line = input.readline()

input.close()
output.close()