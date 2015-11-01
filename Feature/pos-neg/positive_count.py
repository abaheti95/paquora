
import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import csv



def getposCount(sentence,words_posscore):
	text = nltk.word_tokenize(sentence)
	count=0
	for word in text:
		if word in words_posscore:
			count+=1
	return count

def positivity_count(name):
	
	words_posscore={}
	with open('positive_words.csv', 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
	    	words_posscore[row[0]]=1

	f = open(name,'r')
	lines = f.readlines()
	text = ""

	for line in lines:
		text = text + line

	sent_tokenize_list = sent_tokenize(text)
	
	pos_count=0	
	for sent in sent_tokenize_list:
		pos_count+=getposCount(sent,words_posscore)
  	
  	return pos_count