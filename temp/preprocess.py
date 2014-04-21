#!/usr/bin/env python
from nltk.tokenize import *
import re
import nltk.data

#find sentences from a line
def sentenceBound(sentences):
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	return tokenizer.tokenize(sentences)

#find date in the form of '**DATE**'
def dateParse(sentences):
	return re.findall(r'\*\*([0-9.-]+)\*\*', sentences)

#tokenize a sentence
def cleanTokenizer(sentences):
	result = []
	#remove section headers
	index = re.search(r'^[A-Z\s]+\:', sentences)
	if index is not None:
		sentences = index.string[index.end(0):]
	#tokenize by space
	temp_result = WhitespaceTokenizer().tokenize(sentences)
	#remove anywords start or end with symbol
	for item in temp_result:
		if item[-1] == ',':
			item = item[:-1]
		if item[0].isalpha() and item[-1].isalpha():
			result.append(item)
	return result

#read test file
f = open("sample_1.txt","r")

lines = f.readlines()

f.close()
#reading completes

#start cleaning up data

processed = []  #structured data

#record information from the first line
first_line = ""

#count position
total = 1
#start position for each  line as reference
start = 1

for line in lines:

	#count characters
	total = total + len(line)

	#remove all '\n' at the end of a line, the removal won't effect the start position
	line = line.rstrip()

	#remove all space or '\n' at the beginning of a line
	temp_line = line.lstrip()
	
	#if removal, then change the start position of this line
	if len(temp_line) < len(line):
		start = start + len(line) - len(temp_line)
	else:
		pass
	line = temp_line

	#if first line, only record the whole line but not to the structured data (otherwise it will be removed during the following steps)
	if len(first_line) == 0:
		first_line = line
		start = total
		continue

	"""
	clean-up 
	(1) remove all empty lines
	(2) parse paragraphs into sentences
	(3) only record SENTENCES (with a period at the end of the sentence, and has letters)
	"""

	if len(line) > 0:
		#detect sentences
		for temp_line in sentenceBound(line):
			if re.search('[a-zA-Z]', temp_line):	#has words
				if temp_line[-1] == '.':	#end with a period
					#when record a sentence, remove the last period, 'span' is the start position of this sentence in this file
					processed.append({'sentence': temp_line[:-1], 'span': start})
					#start position move to the next sentence	
					start = start + len(temp_line)
	#start position move to the next line
	start = total


"""
pre-processing data
(1) identify date - regular expression "**Date**"
(2) tokenize sentences - ntlk
	- remove section headers: which is not a symptom though may contain SYMPTOM/DIAGNOSIS words
	- remove tokenized items start/end with number/symbols: may not relevant to the output
(3) detect negation, temporal, experiencer (to be implemented) - NegEx ??
"""
for item in processed:
	item['date'] = dateParse(item['sentence'])
	item['content'] = cleanTokenizer(item['sentence'])

r = open("output-1.txt", "w")

for item in processed:
	output = ' '.join(item['content']) + '\n' + '\n'
	r.write(output)
r.close()


for item in processed:
	print item





#ParseDate