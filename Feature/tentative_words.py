"""Returns the number of tentative words in his answers
"""

import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

tentative_list=['may' ,'might','maybe','mightbe','can','could' \
,'perhaps','conceivably','imaginably','resonably','perchance','feasibly',\
'credible','obtainable','probably']

def gettentMeasure(text):	
	sent_tokenize_list = sent_tokenize(text)
	c=0	
	for sent in sent_tokenize_list:
		c+=getTentCount(sent)
  	return c

def getTentCount(sentence):
	text = nltk.word_tokenize(sentence)
	count=0
	for word in text:
		if word in tentative_list:
			count+=1
	return count

def tentative_count(name):
	f = open(name,'r')
	lines = f.readlines()
	text = ""
	for line in lines:
		text = text + line
	return gettentMeasure(text)
