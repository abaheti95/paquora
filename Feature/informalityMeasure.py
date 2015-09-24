"""
I-Measure = (Wrong-typed Words freq. + Interjections freq. + Emoticon freq. ) * 100
Add package enchant
Using nltk package
Currently emoticon parser is not implemented.
"""

import enchant
import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

def getIFMeasure(text):
	wrong_word_count = 0
	interjection_count = 0
	emoticon_count = 0
	sent_tokenize_list = sent_tokenize(text)
	for sent in sent_tokenize_list:
		interjection_count = interjection_count + getInterjectionCount(sent)
		wrong_word_count = wrong_word_count + getWrongWordCount(sent)
		emoticon_count = emoticon_count + getEmoticonCount(sent)
	informality_measure = (interjection_count+wrong_word_count+emoticon_count)*100
  	return (informality_measure,interjection_count,wrong_word_count)

def getInterjectionCount(sentence):
	text = nltk.word_tokenize(sentence)
	print sentence
	tuples = nltk.pos_tag(text)
	intCount = 0
	for t in tuples:
		if t[1]=="UH":
			print "Interjection Word ",t[0]
			intCount = intCount+1
	return intCount

def getWrongWordCount(sentence):
	spell_dict = enchant.Dict("en_US")
	words_list = word_tokenize(sentence.translate(None,string.punctuation))
	wrongCount = 0
	for word in words_list:
		if spell_dict.check(word)==False:
			print "Bad ",word
			wrongCount = wrongCount + 1
	return wrongCount
	#use following for Python 3 instead of above line
	#words_list = word_tokenize(sent.translate(dict.fromkeys(string.punctuation))

def getEmoticonCount(sentence):
	return 0

def getIFMeasureFile(name):
	f = open(name,'r')
	lines = f.readlines()
	text = ""
	for line in lines:
		text = text + line
	return getIFMeasure(text)

