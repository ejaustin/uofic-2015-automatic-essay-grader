import nltk
import os
import sys
from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import wordnet

# ToDo: Record results for each data in the dataset.
# ToDO: Detemine struct for result storage.

# Global vars.
DEBUG = 1

def debug(out):
	if DEBUG:
		print out
	return

# Param: word
# Returns true if the word is illegal, false otherwise.
def double_check(word):
	# Manual spelling mistakes double check.
	manual_set = set(['hyper','global-warming','to','them','his','cannot','they','during','him','should','this',"'ve",'where','because', 'becauase','their','what',"'",'since','your', 'everything','we','how','although','others','would','anything','could','against','you','among','into','everyone','with','everybody','from','.',",",'anyone','until',':',"'s",'than','those','these',"n't",'of','my','and','itself','something','our','themselves','if','!','that','-','ourselves','when','without','which','towards','shall','whether','unless','the','for','whenever','anytime',])
	return word in manual_set

# Spelling mistakes 1a
# Param: file
# Return: number -> correctness value
def spelling_mistakes(testfilename):
	mistakes = []
	data = open(testfilename,'r')
	total = wrong = 0
	for line in data:
		for token in line.split():
			token = token.lower()
			# Verify unknown wordnet tokens against a manual list of legal words.
			if wordnet.synsets(token) == [] and double_check(token) == False:
				mistakes.append(token)
				wrong = wrong+1
			total = total+1
	data.close()
	correctness = 1-(wrong/float(total))
	#ret = '[' + str(wrong) + '][' + str(total) + ']=' + str(correctness)
	#+ str(mistakes)
	#return wrong/float(total)
	return correctness

# Verb Agreement 1b
# Verb Tense 1c
def verb_tense(testfilename):
	present_verbs = ['VBG','VBP','VBZ']
	past_verbs = ['VBD','VBN']
	data = open(testfilename,'r').read();
	tokens = word_tokenize(data)
	pos_tuples = pos_tag(tokens)
	# Collect verb tags from pos tuples.
	verb_tags = []
	for t in pos_tuples:
		if (t[1] in set(present_verbs)) or (t[1] in set(past_verbs)):
			verb_tags.append(t[1])
	# Calculate verb tense correctness.
	vtlength = len(verb_tags)
	wrong = total = 0
	for curr in range(vtlength-1):
		# Check if present verbs match.
		if verb_tags[curr] in set(present_verbs):
			if verb_tags[curr+1]  in set(past_verbs):
				wrong += 1
		# Check if past tense verbs match.
		if verb_tags[curr] in set(past_verbs):
			if verb_tags[curr+1] not in set(present_verbs):
				wrong += 1
		total += 1
	correctness = 1-(wrong/float(total))
	return correctness

# Number of sentences and length 3a
def n_of_sentences(testfilename):
	return

## Get list of tokenized test files.
## Expected path: '../input/test/tokenized'
err = os.chdir('../input/test/tokenized')
path = os.getcwd()
testfileset = os.listdir(path)

for testfilename in testfileset:
	# Check spelling mistakes.
	#score_1a = spelling_mistakes(testfilename)
	#print testfilename + ': ' + str(score_1a)
	# Check verb tense agreement.
	score_1c = verb_tense(testfilename)
	print testfilename + ':' + str(score_1c)