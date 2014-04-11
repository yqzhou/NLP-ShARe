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
	return re.findall(r'\*\*([0-9.-])\*\*', sentences)

#tokenize a sentence
def cleanTokenizer(sentences):
	#remove catogory name
	index = re.search(r'^[A-Z\s]+\:', sentences)
	if index is not None:
		sentences = index.string[index.end(0):]
	#tokenize by space
	temp_result = WhitespaceTokenizer().tokenize(sentences)
	#remove anywords start or end with symbol or number or word with only one letter
	result = []
	for item in temp_result:
		if item[0].isalpha() and item[-1].isalpha() and len(item) > 1:
			result.append(item)
	return result

#read test file
f = open("sample.txt","r")

lines = f.readlines()

f.close()
#reading completes

#start cleaning up data

processed = []
first_line = ""

for line in lines:
	#remove all '\n' at the end of a line
	line = line.rstrip()
	line = line.lstrip()
	if len(first_line) == 0:
		first_line = line
		continue
	#remove all empty lines
	if len(line) > 0:
		#detect sentences
		for temp_line in sentenceBound(line):
			if re.search('[a-zA-Z]', temp_line):
				if temp_line[-1] == '.':
					processed.append({'sentence': temp_line[:-1]})

for item in processed:
	item['date'] = dateParse(item['sentence'])
	item['content'] = cleanTokenizer(item['sentence'])

for item in processed:
	print item['content']



#ParseDate