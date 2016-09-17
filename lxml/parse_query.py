#!/usr/bin/python

import nltk

print "#### INTRO --- ADVERTISEMENT ####"
content = raw_input("How may I help you?\n\n")
tokenized = nltk.word_tokenize(content)
tagged_list = nltk.pos_tag(tokenized)
#print tagged_list

sentnc_list = []
sentnc_list_NN = []
sentnc_list_VB = []

# get all the nouns from the sentence
for entry in tagged_list:
	if "VB" in entry or "VBD" in entry or "VBG" in entry or "VBN" in entry or "VBP" in entry or "VBZ" in entry:
		sentnc_list_VB.append(entry[0])
	elif "NN" in entry or "NNS" in entry or "NNP" in entry or "NNPS" in entry:
		sentnc_list_NN.append(entry[0])

sentnc_list.append(sentnc_list_NN)
sentnc_list.append(sentnc_list_VB)

print sentnc_list
