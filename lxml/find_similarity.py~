#!/usr/bin/python
from nltk.corpus import wordnet as wn


categories = {'places' : wn.synsets('places')[0],
	      'details' : wn.synsets('details')[0],
              'ratings' : wn.synsets('ratings')[0],
              'reviews' : wn.synsets('reviews')[0]}

#find out the similarity score between terms from query and the keys in our data store of states
def get_similarity_score(term):
	try:
		wn_term = wn.synsets(term)[0]
	except:
		#print term
		return
	max_score = -100
	max_sim_key = ''
	for cat, value in categories.iteritems():
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

