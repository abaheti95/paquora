from wordsegment import segment
from nltk import word_tokenize, pos_tag
import numpy as np
import enchant
import nltk
import string
import csv
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re


words_custom = []
sentence_list = []
pos_tags = []

words_posscore = {}
words_neg={}
words_pos={}
func_words=[]
def init():
	global words_posscore
	global words_neg
	global words_pos
	global func_words

	words_posscore = {}
	with open('Feature/pos-neg/words_posscore.csv', 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for row in reader:
			words_posscore[row[0]] = float(row[1])

	words_neg={}
	with open('Feature/pos-neg/negative_words.csv', 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for row in reader:
			words_neg[row[0]] = 1
	
	words_pos={}
	with open('Feature/pos-neg/positive_words.csv', 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for row in reader:
			words_pos[row[0]]=1

	func_words=[]
	with open('Feature/func_words.csv', 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for row in reader:
			func_words.append(row[0])

def get_pos_score(text):
	words = words_custom
	count = 0
	score = 0.0
	for word in words:
		if word in words_posscore:
			count += 1
			score += words_posscore[word]
	if count != 0:
		return (score/count)
	else:
		return 0

def get_neg_count(text):
	words = words_custom
	count = 0
	for word in words:
		if word in words_neg:
			count += 1
	return count

def get_pos_count(text):
	words = words_custom
	count = 0
	for word in words:
		if word in words_pos:
			count += 1
	return count

def get_func_count(text):
	words = words_custom
	count = 0
	for word in words:
		if word in func_words:
			count += 1
		elif any(word in x for x in func_words):
			count += 1
	return count

# Author Ashutosh
# Contributions : WordTokenizer, PreferenceForLongerWordsFeatures, PunctuationsCount
from enchant.tokenize import get_tokenizer, HTMLChunker
def custom_word_tokenize(text):
	tokenizer = get_tokenizer("en_US")
	words = []
	for w in tokenizer(text):
		words.append(w[0])
	return words
	"""# print("Ek baar")
	# First split the text by spaces
	possible_words = text.split()
	# Now use segment function from wordsegment library
	words = []
	for possible_word in possible_words:
		words.extend(segment(possible_word))
	return words"""

"""
Takes the list of words in the text as input and calculates the number of words of length greater than equal 6,7,8,9
:param words: List of strings which are actually words in the text without spaces
:returns: tuple of integer counts
"""
def pref_for_longer_words(text):
	words = words_custom
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
	num_sentences = len(sentence_list)
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

""" Richness in vocabulary
Ref : http://swizec.com/blog/measuring-vocabulary-richness-with-python/swizec/2528
"""
from nltk.stem.porter import PorterStemmer
from itertools import groupby

def vocabulary_richness(text):
	# yule's I measure (the inverse of yule's K measure)
	# higher number is higher diversity - richer vocabulary
	d = {}
	stemmer = PorterStemmer()
	words = words_custom
	for w in words:
		w = stemmer.stem(w).lower()
		try:
			d[w] += 1
		except KeyError:
			d[w] = 1
 
	M1 = float(len(d))
	M2 = sum([len(list(g))*(freq**2) for freq,g in groupby(sorted(d.values()))])
 
	try:
		return (M1*M1)/(M2-M1)
	except ZeroDivisionError:
		return 0

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
	number_sentences = len(sentence_list)
	number_words = len(words_custom)
	return (number_words/number_sentences)
"""
I-Measure = (Wrong-typed Words freq. + Interjections freq. + Emoticon freq. ) * 100
Add package enchant
Using nltk package
Currently emoticon parser is not implemented.
"""
def getIFMeasure(text):
	emoticon_count = getEmoticonCount(text)
	interjection_count = getInterjectionCount(text)
	wrong_word_count = getWrongWordCount(text)
	informality_measure = (interjection_count + wrong_word_count + emoticon_count)*100
	return informality_measure, interjection_count, wrong_word_count

def getInterjectionCount(text):
	tuples = pos_tags
	intCount = 0
	for t in tuples:
		if t[1]=="UH":
			# print "Interjection Word ",t[0]
			intCount = intCount+1
	return intCount

def getWrongWordCount(text):
	US_spell_dict = enchant.Dict("en_US")
	British_spell_dict = enchant.Dict("en_GB")
	words_list = words_custom
	wrongCount = 0
	for word in words_list:
		if US_spell_dict.check(word) == False and British_spell_dict.check(word) == False:
			# print "Bad ",word
			# print("Wrong word : ",word)
			wrongCount = wrongCount + 1
	# print("Wrong word count : ",wrongCount)
	return wrongCount

def test_match(s,essay):
	return essay.count(s)

def getEmoticonCount(text):
	should_match = [
	':)',   # Single smile
	':(',   # Single frown
	':):)', # Two smiles
	':(:(', # Two frowns
	':):(', # Mix of a smile and a frown
	'(*_*)',
	':">',
	';)',
	':D',
	':->',
	':P',
	'<3',
	'</3',
	':O',
	'XD',
	'>:(',
	'D:<',
	'=K',
	':s',
	';P',
	'=)',
	'=O)',
	':-)',
	':^)',
	'=)',
	':O',
	';-)'
	'_/\_',
	'*_*',
	'(* .*)',
	':-?'
	]

	count = 0
	for x in should_match: 
		count = count + test_match(x,text);

	return count
# Author Rahul
# Contributions : TypeByTokenRatio
def gettr_ratio(text):
	words = words_custom
	return len(set(words))*1.0/len(words)

# Author Dhruv
# Contributions : FormalityMeasure, TentativeWords
"""
F-Measure = (noun frequency + adjective freq.   + preposition freq.   + article freq.   -
pronoun freq. - verb freq. - adverb freq. - interjection freq. + 100)/2
"""
def getcounts(text):
	# print sentence
	tuples = pos_tags
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

	result = []
	result = getcounts(text)
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
	words = words_custom
	c = 0
	for word in words:
		if word in tentative_list:
			c += 1
	return c

# Author Sabyasachee
# Contributions : past tense, present tense and future tense counts
def tense_count(text):
	pos_tagged_text = pos_tags
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
	# feature_labels.append("interjection_count")
	feature_labels.append("wrong_word_count")
	# Words Per Sentence
	feature_labels.append("words_per_sentence")
	# Preference to longer words
	feature_labels.append("count_6")
	feature_labels.append("count_7")
	feature_labels.append("count_8")
	feature_labels.append("count_9")
	# # Tentativity
	# feature_labels.append("tentativity")
	# Tense Count
	feature_labels.append("number_past_tense")
	feature_labels.append("number_present_tense")
	# Punctuation Count
	feature_labels.append("number_punctuations")
	# Vocabulary Richness
	feature_labels.append("vocabulary_richness")
	# Positive score
	feature_labels.append("positive_score")
	# # Postive and negative words
	# feature_labels.append("positive_words")
	# feature_labels.append("negative_words")
	# # Functional words
	# feature_labels.append("functional_words")
	# feature_labels.append("emoticons")
	return feature_labels

def get_all_features(text):
	global words_custom
	global sentence_list
	global pos_tags
	words_custom = custom_word_tokenize(text)
	sentence_list = nltk.sent_tokenize(text)
	pos_tags = nltk.pos_tag(words_custom)

	number_words = len(words_custom)
	number_sentences = len(sentence_list)

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
	# features.append(interjection_count / number_words)
	features.append(wrong_word_count / number_words)
	# Words Per Sentence
	words_per_sentence = getWordsPerSentence(text)
	features.append(words_per_sentence)
	# Preference to longer words
	count_6, count_7, count_8, count_9 = pref_for_longer_words(text)
	features.append(count_6 / number_words)
	features.append(count_7 / number_words)
	features.append(count_8 / number_words)
	features.append(count_9 / number_words)
	# # Tentativity
	# tentativity = gettentMeasure(text)
	# features.append(tentativity / number_words)
	# Tense Count
	number_past_tense, number_present_tense = tense_count(text)
	features.append(number_past_tense / number_words)
	features.append(number_present_tense / number_words)
	# Punctuation Count
	number_punctuations = count_punctuations(text)
	features.append(number_punctuations / number_sentences)
	# Vocabulary Richness
	vocabulary_richness_measure = vocabulary_richness(text)
	features.append(vocabulary_richness_measure)
	# Positive score
	positive_score = get_pos_score(text)
	features.append(positive_score)
	# Postive and negative words
	# positive_words = get_pos_count(text)
	# negative_words = get_neg_count(text)
	# features.append(positive_words)
	# features.append(negative_words)
	# # Functional words
	# functional_words = get_func_count(text)
	# features.append(functional_words)

	# emoticon_count = findEmoticonCount(essay)
	# features.append(emoticon_count)
	return features





