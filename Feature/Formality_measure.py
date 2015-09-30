"""
F-Measure = (noun frequency + adjective freq.   + preposition freq.   + article freq.   -
pronoun freq. - verb freq. - adverb freq. - interjection freq. + 100)/2

"""

import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

def getFMeasure(text):
	noun_count = 0 #NN
	adj_count=0 #JJ
	preposition_count=0 #IN
	article_count=0 #a,an ,the
	pronoun_count=0 #PR
	verb_count=0 #VB
	adverb_count=0 #RB
	interjection_count = 0 #UH

	sent_tokenize_list = sent_tokenize(text)
	for sent in sent_tokenize_list:
		result=[]
		result=getcounts(sent)
		noun_count+=result[0]
		adj_count+=result[1]
		preposition_count+=result[2]
		pronoun_count+=result[3]
		verb_count+=result[4]
		adverb_count+=result[5]
		interjection_count+=result[6]
		article_count+=result[7]

	FMeasure = (noun_count+ adj_count  + preposition_count+article_count- pronoun_count - verb_count - adverb_count - interjection_count + 100)/2
	return FMeasure


def getcounts(sentence):
	text = nltk.word_tokenize(sentence)
	print sentence
	tuples=nltk.pos_tag(text)
	noun_count = 0 #NN
	adj_count=0 #JJ
	preposition_count=0 #IN
	article_count=0 #a,an ,the
	pronoun_count=0 #PR
	verb_count=0 #VB
	adverb_count=0 #RB
	interjection_count = 0 #UH
	for t in tuples:
		if 'NN' in t[1]:
			noun_count+=1
		elif 'JJ' in t[1]:
			adj_count+=1
		elif 'IN' in t[1]:
			preposition_count+=1
		elif 'PR' in t[1]:
			pronoun_count+=1;
		elif 'VB' in t[1]:
			verb_count+=1
		elif 'RB' in t[1]:
			adverb_count+=1
		elif 'UH' in t[1]:
			interjection_count+=1
		elif t[0]=="a" or t[0]=="A" or t[0]=="an" or t[0]=="An" or t[0]=="AN" or t[0]=="the" or t[0]=="The" or t[0]=="THE":
			article_count+=1
	result=[]
	result.append(noun_count)
	result.append(adj_count)
	result.append(preposition_count)
	result.append(pronoun_count)
	result.append(verb_count)
	result.append(adverb_count)
	result.append(interjection_count)
	result.append(article_count)
	return result

def FMeasureFile(name):
	f = open(name,'r')
	lines = f.readlines()
	text = ""
	for line in lines:
		text = text + line
	return getFMeasure(text)

