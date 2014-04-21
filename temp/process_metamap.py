#!/usr/bin/env python
import re

checklist = {'Symptom': ['Sign or Symptom', 'Disease or Syndrome', 'Mental Process', 'Pathologic Function'], 'Experiencer': ['Patient or Disabled Group'], 'Temporal': ['Temporal Concept'], 'Body':['Body Part, Organ, or Organ Component', 'Body Location or Region']}

f = open("output-metamap-1.txt")

data = f.readlines()

f.close()

count = 0
line = 0

def new_term(data, index):
	identifier = ''.join(re.findall(r"\[([A-Za-z\s]+)\]", data[index]))
	CUI = ''.join(re.findall(r"(C[0-9]+)\:", data[index]))
	word =''.join(re.findall(r"\:([A-Za-z\s,]+)",data[index]))
	if len(word) > 0:
		return (word, CUI, identifier)
	else:
		return

def new_sentence(data, index, pattern0, pattern1, pattern2):
	identifier = []
	new_identifiers = {}
	index += 1
#	found = False
	while True:
		if index >= len(data) - 1:
			if len(new_identifiers) > 0:
				identifiers.append(new_identifiers)
				return identifiers, index
			break
		if re.search(pattern0, data[index]):
			if len(new_identifiers) > 0:
				identifiers.append(new_identifiers)
				return identifiers, index
			break
		if re.search(pattern1, data[index]):
			if len(new_identifiers) > 0:
				identifiers.append(new_identifiers)
			new_identifiers = {}
			index += 1
			#	found = False
		if index >= len(data) - 1:
			if len(new_identifiers) > 0:
				identifiers.append(new_identifiers)
				return identifiers, index
			break
		if re.search(pattern2, data[index]):
#			found = True
			index += 1
		temp = new_term(data, index)
		if temp is not None:
			(word, CUI, identifier) = temp
			word = word.lower()
			if len(word) > 0 and (word, identifier) not in new_identifiers.keys():
				new_identifiers[(word, identifier)] = CUI
			else:
				pass
			index += 1
		else:
			index += 1
		#index += 1
	return identifiers, index

pattern0 = r"^Processing"
pattern1 = r"^Phrase:"
pattern2 = r"^Meta Mapping"
identifiers = []
result = []

i = 0

while i < len(data) - 1:
	if re.search(pattern0, data[i]):
		identifiers, i = new_sentence(data, i, pattern0, pattern1, pattern2)

for i in range(len(identifiers)):
	for sub_item in identifiers[i]:
		(word, identifier) = sub_item
		CUI = identifiers[i][sub_item]
		if identifier in checklist['Symptom']:
			print i*2 + 1, word, CUI, identifier


			







