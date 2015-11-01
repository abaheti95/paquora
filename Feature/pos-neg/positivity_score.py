
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
			count+=words_posscore['word']
	return count

def positivity_score(name):
	
	words_posscore={}
	with open('words_posscore.csv', 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
	    	words_posscore[row[0]]=float(row[1])


	f = open(name,'r')
	lines = f.readlines()
	text = ""

	for line in lines:
		text = text + line

	sent_tokenize_list = sent_tokenize(text)
	
	pos_score=0	
	for sent in sent_tokenize_list:
		pos_score+=getposCount(sent,words_posscore)
  	
  	return pos_score