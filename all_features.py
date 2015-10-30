from wordsegment import segment
from nltk import word_tokenize, pos_tag
import numpy as np
import enchant
import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# Author Ashutosh
# Contributions : WordTokenizer, PreferenceForLongerWordsFeatures, PunctuationsCount
def custom_word_tokenize(text):
	# First split the text by spaces
	possible_words = text.split()
	# Now use segment function from wordsegment library
	words = []
	for possible_word in possible_words:
		words.extend(segment(possible_word))
	return words

"""
Takes the list of words in the text as input and calculates the number of words of length greater than equal 6,7,8,9
:param words: List of strings which are actually words in the text without spaces
:returns: tuple of integer counts
"""
def pref_for_longer_words(text):
	words = custom_word_tokenize(text)
	count_6 = 0
	count_7 = 0
	count_8 = 0
	count_9 = 0
	for word in words:
		length = len(word)
		if length >= 6:
			count_6 +=  1
		if length >= 7:
			count_7 += 1
		if length >= 8:
			count_8 +=  1
		if length >= 9:
			count_9 += 1
	return count_6, count_7, count_8, count_9

"""
Takes the text and number of sentences as input and counts the number of punctuations in it.
:param text: Complete text. This text should not contain numbers and emojis
:param num_sentences: Number of sentences
:returns: number of punctuations used in the text 
"""
punctuations = ['.', '"',"'",'{','(','-','!','?',':']
def count_punctuations(text):
	num_sentences = len(sent_tokenize(text))
	dots = text.count('.')
	punct_count = 0
	for punctuation in punctuations:
		if punctuation == '.':
			punct_count += num_sentences
		elif punctuation == '"':
			punct_count += int(text.count(punctuation)/2)
		else:
			punct_count += int(text.count(punctuation))
	return punct_count

# Author Nishkarsh
# Contributions : WordsPerSentence
"""
There are two functions in this feature, one takes direct text as input
The other one will take a file name as input and return the words per sentence
The output you will get is: (AverageNumberOfWordsPerSentence, PerSentenceWordCountList[])
I am taking not taking punctuations as words and hence removed it. If you need to migrate to Python 3, then uncomment the line mentioned.
"""
def getWordsPerSentence(text):
	word_count = 0
	word_sent_list = []
	number_sentences = len(sent_tokenize(text))
	number_words = len(custom_word_tokenize(text))
	return (number_words/number_sentences)
"""
I-Measure = (Wrong-typed Words freq. + Interjections freq. + Emoticon freq. ) * 100
Add package enchant
Using nltk package
Currently emoticon parser is not implemented.
"""
def getIFMeasure(text):
	wrong_word_count = 0
	interjection_count = 0
	emoticon_count = 0
	sent_tokenize_list = sent_tokenize(text)
	for sent in sent_tokenize_list:
		interjection_count = interjection_count + getInterjectionCount(sent)
		wrong_word_count = wrong_word_count + getWrongWordCount(sent)
		emoticon_count = emoticon_count + getEmoticonCount(sent)
	informality_measure = (interjection_count + wrong_word_count + emoticon_count)*100
	return informality_measure, interjection_count, wrong_word_count

def getInterjectionCount(sentence):
	text = nltk.word_tokenize(sentence)
	# print sentence
	tuples = nltk.pos_tag(text)
	intCount = 0
	for t in tuples:
		if t[1]=="UH":
			# print "Interjection Word ",t[0]
			intCount = intCount+1
	return intCount

def getWrongWordCount(sentence):
	US_spell_dict = enchant.Dict("en_US")
	British_spell_dict = enchant.Dict("en_GB")
	words_list = custom_word_tokenize(sentence)
	wrongCount = 0
	for word in words_list:
		if US_spell_dict.check(word) == False and British_spell_dict.check(word) == False:
			# print "Bad ",word
			wrongCount = wrongCount + 1
	return wrongCount

def getEmoticonCount(sentence):
	# TODO : This has to be done based on the quora data
	return 0

# Author Rahul
# Contributions : TypeByTokenRatio
def gettr_ratio(text):
	words = custom_word_tokenize(text)
	return len(set(words))*1.0/len(words)

# Author Dhruv
# Contributions : FormalityMeasure, TentativeWords
"""
F-Measure = (noun frequency + adjective freq.   + preposition freq.   + article freq.   -
pronoun freq. - verb freq. - adverb freq. - interjection freq. + 100)/2
"""
def getcounts(sentence):
	text = nltk.word_tokenize(sentence)
	# print sentence
	tuples = nltk.pos_tag(text)
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
		result = []
		result = getcounts(sent)
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

tentative_list=['may' ,'might','maybe','mightbe','can','could' \
,'perhaps','conceivably','imaginably','resonably','perchance','feasibly',\
'credible','obtainable','probably']

def gettentMeasure(text):	
	words = custom_word_tokenize(text)
	c = 0
	for word in words:
		if word in tentative_list:
			c += 1
	return c

# Author Sabyasachee
# Contributions : past tense, present tense and future tense counts
def tense_count(text):
	words = nltk.word_tokenize(text)
	pos_tagged_text = pos_tag(words)
	VB = []
	VBD = []
	VBG = []
	VBN = []
	VBP = []
	VBZ = []
	Others = []
	for (word, tag) in pos_tagged_text:
		if tag == "VB":
			VB.append(word)
		elif tag == "VBD":
			VBD.append(word)
		elif tag == "VBG":
			VBG.append(word)
		elif tag == "VBN":
			VBN.append(word)
		elif tag == "VBP":
			VBP.append(word)
		elif tag == "VBZ":
			VBZ.append(word)
		elif tag.find("VB") != -1:
			Others.append(word)
	number_past_tense = len(VBD) + len(VBP)
	number_present_tense = len(VBG)
	return number_past_tense, number_present_tense

def get_all_feature_labels():
	feature_labels = []
	# Type By Token Ratio
	feature_labels.append("type_by_token_ratio")
	# F-Measure
	feature_labels.append("f_measure")
	# I-Measure
	feature_labels.append("i_measure")
	feature_labels.append("interjection_count")
	feature_labels.append("wrong_word_count")
	# Words Per Sentence
	feature_labels.append("words_per_sentence")
	# Preference to longer words
	feature_labels.append("count_6")
	feature_labels.append("count_7")
	feature_labels.append("count_8")
	feature_labels.append("count_9")
	# Tentativity
	feature_labels.append("tentativity")
	# Tense Count
	feature_labels.append("number_past_tense")
	feature_labels.append("number_present_tense")
	# Punctuation Count
	feature_labels.append("number_punctuations")
	return feature_labels

def get_all_features(text):
	global words_nltk
	global words_custom
	words_nltk = nltk.word_tokenize(text)
	words_custom = custom_word_tokenize(text)
	
	features = []
	# Type By Token Ratio
	type_by_token_ratio = gettr_ratio(text)
	features.append(type_by_token_ratio)
	# F-Measure
	f_measure = getFMeasure(text)
	features.append(f_measure)
	# I-Measure
	i_measure, interjection_count, wrong_word_count = getIFMeasure(text)
	features.append(i_measure)
	features.append(interjection_count)
	features.append(wrong_word_count)
	# Words Per Sentence
	words_per_sentence = getWordsPerSentence(text)
	features.append(words_per_sentence)
	# Preference to longer words
	count_6, count_7, count_8, count_9 = pref_for_longer_words(text)
	features.append(count_6)
	features.append(count_7)
	features.append(count_8)
	features.append(count_9)
	# Tentativity
	tentativity = gettentMeasure(text)
	features.append(tentativity)
	# Tense Count
	number_past_tense, number_present_tense = tense_count(text)
	features.append(number_past_tense)
	features.append(number_present_tense)
	# Punctuation Count
	number_punctuations = count_punctuations(text)
	features.append(number_punctuations)

	return features
