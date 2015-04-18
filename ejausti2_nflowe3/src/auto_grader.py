import nltk
import os
import re
import sys
from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize


# ToDo: Record results for each data in the dataset.
# ToDO: Detemine struct for result storage.


# Global vars.
DEBUG = 1
present_verbs = {'VBG','VBP','VBZ'}
past_verbs = {'VBD','VBN'}

singular_noun = ["NN", "NNP"]
plural_noun = ["NNS", "NNPS"]

singular_verb = "VBZ"
plural_verb = "VBP"
modals = ["can", "cant", "couldn't", "could", "may", "might", "will",\
        "won't", "would", "wouldn't", "must", "shall", "should"]


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
#Param: Test data tokens
# Return: number (correctness value)
def verb_agreement(tokens):
	num_verbs = 0
	errors = 0
	# Tag the tokens.
	lexical_tag_list = pos_tag(tokens)
	# Collect pos tags from tagged tokens.
	pos_tags = [tag[1] for tag in lexical_tag_list]
	length = len(pos_tags)
	for index in range(length-1):
	    # We want to count the total number of verbs in the text
	    if pos_tags[index] == singular_verb or pos_tags[index] == plural_verb:
	    	num_verbs += 1
	    # If there is a modal verb such as can, may or might, we need to
	    # have a verb in the base form without any inflection.
	    # (Below) Because plural verbs in English have no inflection.
	    if tokens[index] in modals and pos_tags[index + 1] != "VB":
	        errors += 1
	    # If the noun or pronoun is singular in number but followed by a
	    # plural verb, we increment the number of errors.
	    if pos_tags[index] in singular_noun or tokens[index] == 'he' or tokens[index] == 'she' or tokens[index] == 'it':
		if pos_tags[index + 1] == plural_verb:
			errors += 1
	    # Else if the noun or pronoun is plural and followed with a singular verb,
	    # we increment the number of errors
	    elif pos_tags[index] in plural_noun and pos_tags[index + 1] == singular_verb:
			errors += 1
	correctness = 1-(errors/float(num_verbs))
	return correctness

# Verb Tense 1c
# Param: Test data tokens
# Return: number (correctness value)
def verb_tense(tokens):
	sentences = sent_tokenize(data)
	pos_tuples = pos_tag(tokens)
	# Collect verb tags from pos tuples.
	# Can be used to count total number of verbs
	verb_tags = [tag[1] for tag in pos_tuples if tag[1] in present_verbs or tag[1] in past_verbs]
	# We want to count how many of each tense of verb are in the essays.
	present_tags = [p for p in verb_tags if p in present_verbs]
	past_tags = [p for p in verb_tags if p in past_verbs]
	# Here we are creating a list that contains a sentence that has been pos-tagged for each index.
	# (Below) Tags for a single sentence.
	sentence_tags = []
	# Tags for the whole document.
	sen = []
	for sentence in sentences:
		sentence_tags = pos_tag(word_tokenize(sentence))
		sen.append(sentence_tags)
	pres = False
	past = False
	inconsistencies = 0
	for sentence in sen:
		for word in sentence:
			# Count the number of present tense verbs and past tense verbs.
			if word[1] in present_verbs:
				pres = True
			if word[1] in past_verbs:
				past = True
		# Add one to inconsistencies if a sentence has both past and present tense.
		if pres and past:
			inconsistencies += 1
			pres = False
			past = False
	correctness = 1-(inconsistencies/float(len(sen)))
	return correctness


# Number of sentences and length 3a
# Param: Test data. Not tokenized.
# Return: Lexical richness of the document (lengths of sentences).
def n_of_sentences(data):
	# The words must contain letters or digits
	nonPunct = re.compile('.*[A-Za-z0-9].*')
	# Tokenize data for sentences.
	sents = sent_tokenize(data)
	tokens_raw = word_tokenize(data)
	# Count the number of words.
	filtered_words = [w for w in tokens_raw if nonPunct.match(w)]
	num_sents = len(sents)
	num_words = len(filtered_words)
	return num_words/float(num_sents)

''' Code execute block. '''
## Get list of tokenized test files.
## Expected path: '../input/test/tokenized'
err = os.chdir('/input/test/tokenized')
path = os.getcwd()
testfileset = os.listdir(path)

for testfilename in testfileset:
	# Open the test file and tokenize the data.
	testfile = open(testfilename,'r')
	data = testfile.read();
	tokens = word_tokenize(data)

	# Check the spelling mistakes.
	score_1a = spelling_mistakes(tokens)
	# Check the verb agreement.
	score_1b = verb_agreement(tokens)
	# Check the verb tense agreement.
	score_1c = verb_tense(tokens)
	# Count the number of sentences.
	score_3a = n_of_sentences(data)

	# Final operations.
	testfile.close()
	#print testfilename + '\t' + str(score_1a) + '\t' +\
	#	str(score_1b) + '\t' + str(score_1c) + '\t' + str(score_3a)
	print score_1b