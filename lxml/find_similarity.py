#!/usr/bin/python
from nltk.corpus import wordnet as wn

synset_keys = {'price' : wn.synsets('price')[0],
					 'food' : wn.synsets('food')[0],
					 'ambience' : wn.synsets('ambience')[0],
					 'service' : wn.synsets('service')[0]}


# find out the similarity score between terms from query and the keys in our data store of states
def detect_similarity(term):
	try:
		wn_term = wn.synsets(term)[0]
	except:
		return

	max_score = -100
	max_sim_key = ''
	for cat, value in synset_keys.iteritems():
		sim_score = wn.wup_similarity(wn_term, value)
		#print cat, term, sim_score
		if sim_score > max_score:
			max_score = sim_score
			max_sim = cat

	temp = []
	temp.append(max_sim)
	temp.append(max_score)

	if temp[1] >= 0.5:
		return temp
	else:
		return

