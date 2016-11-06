from find_similarity import get_similarity_score
from nltk.corpus import wordnet as wn

qry_terms = dict()

#want to travel from Mumbai to Mount Abu guide me
query="tell me the details about places to visit in Rajasthan"
#use pos tagged list, prepared in parse_query.py file

list_of_terms = query.split(" ");

#append synsets for terms
for term in list_of_terms:
	for i in wn.synsets(term):
		key=wn.morphy(term)
                for j in i.lemmas():  # Iterating through lemmas for each synset.
			# append synonyms
			syn = str(j.name())
			if key in qry_terms:
    				qry_terms[key].append(syn)
			else:
        			# create a new array in this slot
        			qry_terms[key] = [syn]

for c in qry_terms:
	qry_terms[c] = list(set(qry_terms[c]))
	#print c, ':', qry_terms[c]
print qry_terms

for cat, val_lst in qry_terms.iteritems():
	for entry in val_lst:
		print entry ,get_similarity_score(entry)

