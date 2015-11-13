from __future__ import division
import re
from enchant.tokenize import get_tokenizer, HTMLChunker, URLFilter, WikiWordFilter
from gensim import corpora, models
import gensim
import numpy
import MySQLdb as mdb

'''
	read the quora answers
'''
inputFile = open("corpus.txt", "r")
corpustext = inputFile.read()
documents = re.split("&+\n", corpustext)
inputFile.close()
print "quora answers read"

'''
	create the processed documents 
'''
processed_documents = []
chunkers = [HTMLChunker]
filters = [URLFilter,WikiWordFilter]
tokenizer = get_tokenizer("en_US",chunkers,filters)
count = 0
for document in documents:
	try:
		if document is not None:
			lowered_document = document.strip().lower()
			processed_document = []
			for word in tokenizer(document):
				word = "".join(i for i in word[0] if ord(i)<128)
				if len(word) > 0:
					processed_document.append(word)
			if len(processed_document) > 0:
				processed_documents.append(processed_document)
				count += 1
				if count in [100,1000,5000,10000,20000,30000,50000,75000,100000]:
					print count, "documents processed"
	except Exception:
		print "some error with document"
print "All documents processed"

'''
	read the LIWC words from mysql
'''
liwc = {}
db = mdb.connect("localhost", "nlp", "nlppassword", "nlp")
cursor = db.cursor()
cursor.execute("select word, type from LIWC")
for word, category in cursor:
	if category not in liwc.keys():
		liwc[category] = set()
	liwc[category].add(word)
print "liwc words are read"
db.close()

'''
	create the dictionary, document - term matrix, collection_frequencies matrix
'''

dictionary = corpora.Dictionary(processed_documents)
print "dictionary created"
corpus = [dictionary.doc2bow(text) for text in processed_documents]
print "document term matrix created"
collection_frequencies = {}
max_collection_frequency = 0
for document in corpus:
	for (wordid, frequency) in document:
		if wordid not in collection_frequencies:
			collection_frequencies[wordid] = 0
		collection_frequencies[wordid] = collection_frequencies[wordid] + frequency
print "collection_frequencies calculated"
# max_collection_frequency = max(collection_frequencies.values())
# for key, value in collection_frequencies.iteritems():
# 	collection_frequencies[key] = value/max_collection_frequency
# print "collection_frequencies matrix normalised"

'''
	create quoravocabulary, and eta parameter
'''
quoravocabulary = set(dictionary.values())
print quoravocabulary
topics = liwc.keys()
num_topics = len(topics)
num_words = len(quoravocabulary)
eta = numpy.full(shape = (num_topics, num_words), dtype = float, fill_value = 0.01)
for topic_number,topic in enumerate(topics):
	liwc_words = liwc[topic]
	print topic, "="
	intersection_words = quoravocabulary & liwc_words
	for word in intersection_words:
		print word,
		wordid = dictionary.token2id[word]
		eta[topic_number][wordid] = collection_frequencies[wordid]
	print
	print
print "eta parameter created"
'''
	running lda model
'''
print "lda process begins"
ldamodel = gensim.models.ldamulticore.LdaMulticore(corpus, num_topics = num_topics, 
	id2word = dictionary, passes = 20, eta = eta, workers = 8)
print "lda process done"

'''
	saving output in File
'''
outputFile = open("output.txt", "w")
ldaresult = ldamodel.show_topics(num_topics = num_topics, num_words = 1000, formatted = False)
for topic_number,result in enumerate(ldaresult):
	result = sorted(result, key = lambda x: x[0], reverse = True)
	topic = topics[topic_number]
	words = set()
	min_probability = None
	max_probability = None
	for probability, word in result:
		if probability < 0.05:
			break
		if word not in liwc[topic]:
			words.add(word)
			if min_probability is None or min_probability > probability:
				min_probability = probability
			if max_probability is None or max_probability < probability:
				max_probability = probability
	print topic, "= min:", min_probability, " max:", max_probability
	outputFile.write(topic)
	outputFile.write("\n")
	for word in words:
		outputFile.write(word)
		outputFile.write(",")
	outputFile.write("\n")
outputFile.close()
print "results are saved"