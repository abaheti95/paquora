import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

"""
There are two functions in this feature, one takes direct text as input
The other one will take a file name as input and return the words per sentence
The output you will get is: (AverageNumberOfWordsPerSentence, PerSentenceWordCountList[])
I am taking not taking punctuations as words and hence removed it. If you need to migrate to Python 3, then uncomment the line mentioned.
"""
def getWordsPerSentence(text):
	word_count = 0
	word_sent_list = []
	sent_tokenize_list = sent_tokenize(text)
	for sent in sent_tokenize_list:
		words_list = word_tokenize(sent.translate(None,string.punctuation))
		#use following for Python 3 instead of above line
		#words_list = word_tokenize(sent.translate(dict.fromkeys(string.punctuation))
		word_sent_list.append(len(words_list))
		word_count = word_count+len(words_list)
	word_per_sentence = word_count/len(sent_tokenize_list)
	return (word_per_sentence,word_sent_list)

def getWordsPerSentenceFromFile(name):
	f = open(name,'r')
	lines = f.readlines()
	text = ""
	for line in lines:
		text = text + line
	return getWordsPerSentence(text)

if __name__ == '__main__':
	main()
