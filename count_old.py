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
			e_param[("_RARE_",key)] = float(e_count[("_RARE_",key)])/float(u_count[key])

def trans_param(b_count, t_count, t_param):
	for key in t_count:
		t_param[(key[2],key[0],key[1])] = float(t_count[key])/b_count[(key[0],key[1])]
	

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

#run count_freqs again and open gene.count to read counts

try:
	in_count = open("gene.count","r")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

#initialize dictionaries for count(y~>x), unigram, bigram and trigram counts

e_count = defaultdict(int)
u_count = defaultdict(int)
b_count = defaultdict(int)
t_count = defaultdict(int)

#dictionary for emission parameters
e_param = defaultdict(float)

#read counts in resp dictionaries
line = in_count.readline()
while(line):
	if line != "\n":
		words = line.split()
		if words[1] == "WORDTAG":
			e_count[(words[3],words[2])] = int(words[0])
		elif words[1] == "1-GRAM":
			u_count[words[2]] = int(words[0])
		elif words[1] == "2-GRAM":
			b_count[(words[2],words[3])] = int(words[0])
		elif words[1] == "3-GRAM":
			t_count[(words[2],words[3],words[4])] = int(words[0])
		else:
			print("Error -->",words[1])
			exit(1)
		
	line = in_count.readline()

in_count.close()
input.close()

#part 1 open gene.dev and out file
try:
	input = open("gene.test","r")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

try:
	output = open("gene_dev.p1.out","w")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

#calculate the emission parameters
emmission_param(e_count,u_count,e_param,count)

#tag the input and write to out file
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

output.close()

#dictionary for transmission parameters
t_param = defaultdict(float)

#calculate the transmission parameters
trans_param(b_count, t_count, t_param)

Slis = []
for k in u_count:
	Slis.append(k)

try:
	output = open("gene_dev.p2.out","w")
except IOError:
	sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
	sys.exit(1)

#rset file pointer to start of file
input.seek(0,0)
line = input.readline()
while line:
	max_prob = defaultdict(float)
	bp = defaultdict(str)
	y = defaultdict(str)
	max_prob[(0,"*","*")] = 1
	sent = defaultdict(str)
	orig_sent = defaultdict(str)
	i = 0
	S = defaultdict(set)
	S[-1] = set('*')
	S[0] = set('*')
	while line!="\n":
		i += 1
		orig_sent[i] = line.splitlines()[0]
		sent[i] = line.splitlines()[0]
		S[i] = set(Slis)
		line = input.readline()
	for k in sent:
		for u in S[k-1]:
			for v in S[k]:
				max_prob[(k,u,v)] = -1
				for w in S[k-2]:
					if(sent[k] in count and count[sent[k]]>=5):
						t = max_prob[(k-1,w,u)]*t_param[(v,w,u)]*e_param[(sent[k],v)]
						if(t>=max_prob[(k,u,v)]):
							max_prob[(k,u,v)] = t
							bp[(k,u,v)] = w
					else:
						t = max_prob[(k-1,w,u)]*t_param[(v,w,u)]*e_param[("_RARE_",v)]
						if(t>max_prob[(k,u,v)]):
							max_prob[(k,u,v)] = t
							bp[(k,u,v)] = w
	t = -1
	for u in S[i-1]:
		for v in S[i]:
			m = max_prob[(i,u,v)]*t_param[("STOP",u,v)]
			if(m>=t):
				t = m
				y[i-1] = u
				y[i] = v
	for j in range(2,i):
		k = i - j
		y[k] = bp[k+2,y[k+1],y[k+2]]
	for k in orig_sent:
		output.write(orig_sent[k]+" "+y[k]+"\n")
	output.write("\n")
	line = input.readline()

input.close()
output.close()
