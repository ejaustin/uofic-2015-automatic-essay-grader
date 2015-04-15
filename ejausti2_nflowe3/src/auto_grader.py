import nltk
import os
import sys
from nltk.corpus import wordnet

# ToDo: Record results for each data in the dataset.
# ToDO: Detemine struct for result storage.

# Global vars.
DEBUG = 1
# Manual spelling mistakes double check.
manual_set = set(['hyper','global-warming','to','them','his','cannot','they','during','him','should','this',"'ve",'where','because', 'becauase','their','what',"'",'since','your', 'everything','we','how','although','others','would','anything','could','against','you','among','into','everyone','with','everybody','from','.',",",'anyone','until',':',"'s",'than','those','these',"n't",'of','my','and','itself','something','our','themselves','if','!','that','-','ourselves','when','without','which','towards','shall','whether','unless','the','for','whenever','anytime',])

def debug(out):
	if DEBUG:
		print out
	return

# Param: word
# Returns true if the word is illegal, false otherwise.
def double_check(word):
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

# Agreement 1b
# Verbs 1c
# Number of sentences and length 3a

## Get list of tokenized test files.
## Expected path: '../input/test/tokenized'
err = os.chdir('../input/test/tokenized')
path = os.getcwd()
testfileset = os.listdir(path)

for testfilename in testfileset:
	# Check spelling mistakes.
	score_1a = spelling_mistakes(testfilename)
	print testfilename + ': ' + str(score_1a)