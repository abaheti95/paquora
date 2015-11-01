import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import csv
from  __builtin__ import any as b_any

def getfuncCount(sentence,func_words):
	text = nltk.word_tokenize(sentence)
	count=0
	for word in text:
		if word in func_words:
			count+=1
		elif b_any(word in x for x in func_words):
			count+=1
	return count

def func_count(name):
	
	func_words={}
	with open('func_words.csv', 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
	    	func_words.append(row[0])

	f = open(name,'r')
	lines = f.readlines()
	text = ""

	for line in lines:
		text = text + line

	sent_tokenize_list = sent_tokenize(text)
	
	func_count=0	
	for sent in sent_tokenize_list:
		func_count+=getfuncCount(sent,func_words)
  	
  	return func_count