import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
 
text = open('test.txt', 'r').read()
nonPunct = re.compile('.*[A-Za-z0-9].*')   # the words must contain letters or digits
 
def sentence_count():
        sents = sent_tokenize(text)
        tokens_raw = word_tokenize(text)
 
        filtered_words = [w for w in tokens_raw if nonPunct.match(w)]
 
        num_sents = len(sents)
        num_words = len(filtered_words)
 
        print(filtered_words)
        print("There are %d sentences in total and %d words" % (num_sents, num_words))
 
 
sentence_count()