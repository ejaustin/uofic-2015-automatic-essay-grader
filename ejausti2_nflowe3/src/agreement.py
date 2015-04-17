import nltk
from nltk import pos_tag
from nltk import word_tokenize
 
singular_noun = ["NN", "NNP"]
plural_noun = ["NNS", "NNPS"]

singular_verb = "VBZ"
plural_verb = "VBP"
modals = ["can", "cant", "couldn't", "could", "may", "might", "will", "won't", "would", "wouldn't", "must", "shall", "should"]


text = open('test.txt', 'r').read()


def compute_errors():
        num_verbs = 0
        errors = 0
 
        tokens = word_tokenize(text)
        lexical_tag_list = pos_tag(tokens)
        pos_tags = [tag[1] for tag in lexical_tag_list]
        length = len(pos_tags)
 	print pos_tags
        for index in range(length):
 
                # We don't want to get an out of bounds error
                if index == length - 1:
                        break
 
                # We want to count the total number of verbs in the text
                if pos_tags[index] == singular_verb or pos_tags[index] == plural_verb:
                        num_verbs += 1
                        #print(tokens[index - 1] + " " + tokens[index])
 
                # If there is a modal verb such as can, may or might, we need to have a verb in the base form without any inflection
                if tokens[index] in modals and pos_tags[index + 1] != "VB":   # Because plural verbs in English have no inflection
                        errors += 1
                        #print(tokens[index] + " " + pos_tags[index + 1] + "Type 1")
 
                # If the noun or pronoun is singular in number but followed by a plural verb, we increment the number of errors
                if pos_tags[index] in singular_noun or tokens[index] == 'he' or tokens[index] == 'she' or tokens[index] == 'it':
                        if pos_tags[index + 1] == plural_verb:
                                errors += 1
                                #print(tokens[index] + " " + tokens[index + 1] + "Type 2")
 
                # Else if the noun or pronoun is plural and followed with a singular verb, we increment the number of errors
                elif pos_tags[index] in plural_noun and pos_tags[index + 1] == singular_verb:
                        errors += 1
                        #print(tokens[index] + " " + tokens[index + 1] + "Type 3")
 
                #print("Index number %d out of %d." % (index, len(pos_tags)))
 
        return errors / num_verbs
 
grade = compute_errors()
grade *= 100
print("{:1.2f}".format(grade) + "% of the verbs are not inflected properly.")
