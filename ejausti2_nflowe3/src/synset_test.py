import nltk
import os
import re
import sys
from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize

''' Main code block. '''
## Testing word similarity using wordnet
#dog = wordnet.synset('dog.n.01')
#cat = wordnet.synset('cat.n.01')
#print dog.path_similarity(cat)
things = ['car', 'gas', 'map', 'road']
wordnet_things = []
# Grab synset for tokens in things
for token in things:
	word = wordnet.synsets(token)
	if word != []:
		wordnet_things.append(word[0])
# Check similarity for tokens in wordnet_things
for t1 in wordnet_things:
	for t2 in wordnet_things:
		if t1 != t2:
			print '[' + str(t1) + '][' + str(t2) + '], ' +\
			str(t1.path_similarity(t2)) + ' ' + str(t1.lch_similarity(t2)) + ' ' +\
			str(t1.wup_similarity(t2))
			# Requires a Information Content IC
			#str(t1.res_similarity(t2))

# Similarity function
def similarity(tagged_lexicon):
	noun_list = []
	# Add nouns to the noun_list.
	for token in tagged_lexicon:
		if token[1] == singular_noun or token[1] == plural_noun:
			noun_list.append(token[0])
	# Todo: determine which word to take from the synset list.
	bound = len(noun_list)
	for i in range(bound-1):
		for j in range(i+1, bound-1):
			sim = noun_list[i].lch_similarity(noun_list[j])
			# Todo: determine threshold for similarity scoring.
