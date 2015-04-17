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
present_verbs = {'VBG','VBP','VBZ'}
past_verbs = {'VBD','VBN'}


def debug(out):
	if DEBUG:
		print out
	return


# Param: word
# Return: True if the word is illegal, false otherwise.
def double_check(word):
	# Manual spelling mistakes double check.
	manual_set = set(['hyper','global-warming','to','them','his','cannot','they',\
		'during','him','should','this',"'ve",'where','because', 'becauase','their',\
		'what',"'",'since','your', 'everything','we','how','although','others','would',\
		'anything','could','against','you','among','into','everyone','with','everybody',\
		'from','.',",",'anyone','until',':',"'s",'than','those','these',"n't",'of','my',\
		'and','itself','something','our','themselves','if','!','that','-','ourselves',\
		'when','without','which','towards','shall','whether','unless','the','for',\
		'whenever','anytime',])
	return word in manual_set


# Spelling mistakes 1a
# Param: Test data tokens
# Return: number (correctness value)
def spelling_mistakes(tokens):
	total = wrong = 0
	for token in tokens:
		token = token.lower()
		# Verify unknown wordnet tokens against a manual list of legal words.
		if wordnet.synsets(token) == [] and double_check(token) == False:
			# Increment wrong count if the token is not valid.
			wrong = wrong+1
		total = total+1
	correctness = 1-(wrong/float(total))
	return correctness


# Verb Agreement 1b


# Verb Tense 1c
# Param: Test data tokens
# Return: number (correctness value)
def verb_tense(tokens):
	# Tagg the tokens.
	pos_tuples = pos_tag(tokens)
	# Collect verb tags from pos tuples.
	verb_tags = [t[1] for t in pos_tuples if t[1] in present_verbs or t[1] in past_verbs]
	# Calculate verb tense correctness.
	vtlength = len(verb_tags)
	wrong = total = 0
	for curr in range(vtlength-1):
		# Check if present verbs match.
		if verb_tags[curr] in present_verbs:
			if verb_tags[curr+1] in past_verbs:
				wrong += 1
		# Check if past tense verbs match.
		if verb_tags[curr] in past_verbs:
			if verb_tags[curr+1] in present_verbs:
				wrong += 1
		total += 1
	correctness = 1-(wrong/float(total))
	return correctness


# Number of sentences and length 3a
def n_of_sentences(testfilename):
	return

''' Code execute block. '''
## Get list of tokenized test files.
## Expected path: '../input/test/tokenized'
err = os.chdir('../input/test/tokenized')
path = os.getcwd()
testfileset = os.listdir(path)

for testfilename in testfileset:
	# Open the test file and tokenize the data.
	testfile = open(testfilename,'r')
	data = testfile.read();
	tokens = word_tokenize(data)

	# Check spelling mistakes.
	score_1a = spelling_mistakes(tokens)
	# Check verb tense agreement.
	score_1c = verb_tense(tokens)

	# Final operations.
	testfile.close()
	print testfilename + '\t' + str(score_1a) + '\t' + str(score_1c)