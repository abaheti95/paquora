
import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import csv



def getnegCount(sentence,words_negscore):
	text = nltk.word_tokenize(sentence)
	count=0
	for word in text:
		if word in words_negscore:
			count+=1
	return count

def negativity_count(name):
	
	words_negscore={}
	with open('negative_words.csv', 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
	    	words_negscore[row[0]]=1

	f = open(name,'r')
	lines = f.readlines()
	text = ""

	for line in lines:
		text = text + line

	sent_tokenize_list = sent_tokenize(text)
	
	neg_count=0	
	for sent in sent_tokenize_list:
		neg_count+=getnegCount(sent,words_negscore)
  	
  	return neg_count