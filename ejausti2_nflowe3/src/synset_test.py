import nltk
import os
import re
import sys
from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize


singular_noun = {"NN", "NNP"}
plural_noun = {"NNS", "NNPS"}

singular_verb = "VBZ"
plural_verb = "VBP"

base_synsets = []


# Initialize base synsets.
def init_synsets():
	base_words = ['car.n.01', 'technology.n.01', 'gasoline.n.01', 'fuel.n.01', 'transportation.n.02',\
					'price.n.03', 'risk.n.03', 'future.n.01', 'today.n.01', 'man.n.03']
	for word in base_words:
		syn = wordnet.synset(word)
		base_synsets.append(syn)
		#print syn


def topic_coherence(lexical_tag_list):
	# Collect topic words.
	topic_synsets = []
	topic_sims = []
	for token in lexical_tag_list:
		if token[1] in singular_noun or token[1] in plural_noun: # or token[1] == singular_verb or token[1] == plural_verb):
			syn = wordnet.synsets(str(token[0]))
			if syn != []:
				topic_synsets.append(syn)
	# Collect one most significant similarity for each topic synsets.
	# topic is a list of synsets
	# syn is a single synset in the topic
	for topic in topic_synsets:
		sims = []
		for syn in topic:
			if ".n." in str(syn):
				for b in base_synsets:
					sims.append(syn.lch_similarity(b))
		print str(topic[0]) + ': ' + str(len(sims))
		if sims != []:
			topic_sims.append(max(sims))
	print str(topic_sims)



## Get list of tokenized test files.
## Expected path: '../input/test/tokenized'
err = os.chdir('test')
path = os.getcwd()
testfileset = os.listdir(path)
results = []
init_synsets()
for testfilename in testfileset:
	print testfilename
	# Open the test file and tokenize the data.
	testfile = open(testfilename,'r')
	data = testfile.read();
	tokens = word_tokenize(data)
	# Tag the tokens.
	lexical_tag_list = pos_tag(tokens)
	topic_coherence(lexical_tag_list)
	print "Done."


'''
for t1 in wordnet_synsets:
	for t2 in wordnet_synsets:
		if t1 != t2:
			print '[' + str(t1) + '][' + str(t2) + '], ' +\
			str(t1.path_similarity(t2)) + ' ' + str(t1.lch_similarity(t2)) + ' ' +\
			str(t1.wup_similarity(t2))
			# Requires a Information Content IC
			#str(t1.res_similarity(t2))
'''
# Similarity function
'''
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
'''


'''
car technology gas oil fuel transport
resource cost industry risk
future today man
car future today economy technology commute concern society gas resource oil cost fuel
automobile civilization today car movement world economy social technology users growth rate advancement less more road
	company world today industry future oil business alternative fuel development
automibile pollution fuel resource car man people transport earth planet price excess effect human depletion
	engines generation travel
world car twenty years automobile market sales higher oil world fuel enviornment pollution rate resource price energy
    market transport system choice decision  accident negative positive human race materialistic traffic buying road
    congestion
 generation car living luxury comfort public transport pollution number car manufacture human race
'''