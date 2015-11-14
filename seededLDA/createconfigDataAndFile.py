import re
from enchant.tokenize import get_tokenizer, HTMLChunker, URLFilter, WikiWordFilter
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
	process the documents
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
					processed_document.append(word.lower())
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
	create the config data and config file
'''
word2id = {}
vocabulary = set()
vocablength = 0
wordindicesfile = open("/Users/Sabyasachee/Downloads/SeededLDA/data/wordindices.txt","w")
docindicesfile = open("/Users/Sabyasachee/Downloads/SeededLDA/data/docindices.txt","w")
wordsfile = open("/Users/Sabyasachee/Downloads/SeededLDA/data/words.txt","w")
seedwordsfile = open("/Users/Sabyasachee/Downloads/SeededLDA/data/seedwords.txt","w")
configfile = open("/Users/Sabyasachee/Downloads/SeededLDA/data/config","w")

wordsfilestring = ""
wordindicesfilestring = ""
docindicesfilestring = ""

for docid, document in enumerate(processed_documents):
	for token in document:
		if token not in vocabulary:
			vocablength = vocablength + 1
			word2id[token] = vocablength
			vocabulary.add(token)
			wordsfilestring += token + "\n"
		wordindicesfilestring += str(word2id[token]) + "\n"
		docindicesfilestring += str(docid+1) + "\n"
	if docid in [100,1000,5000,10000,20000,30000,50000,75000,100000]:
		print docid, "documents written"

wordindicesfile.write(wordindicesfilestring)
wordsfile.write(wordsfilestring)
docindicesfile.write(docindicesfilestring)

topics = liwc.keys()
for topic in topics:
	text = ""
	count =  20 if 20 < len(liwc[topic]) else len(liwc[topic])
	c = 0
	for w in liwc[topic] & vocabulary:
		text += w + ","
		c += 1
		if c == count:
			break
	seedwordsfile.write(text[:-1] + "\n")
configfile.write("sSrcWordIndices /Users/Sabyasachee/Downloads/SeededLDA/data/wordindices.txt\n")
configfile.write("sSrcDocIndices /Users/Sabyasachee/Downloads/SeededLDA/data/docindices.txt\n")
configfile.write("sSrcWords /Users/Sabyasachee/Downloads/SeededLDA/data/words.txt\n")
configfile.write("iNoTopics 64\n")
configfile.write("iNoIterations 100\n")
configfile.write("dAlpha 1.0\n")
configfile.write("dBeta 0.01\n")
configfile.write("dMu0 1e-7\n")
configfile.write("dTau0 0.7\n")
configfile.write("bAllowSeedWords 1\n")
configfile.write("sSeedTopicalWordsPath /Users/Sabyasachee/Downloads/SeededLDA/data/seedwords.txt\n")
wordindicesfile.close()
docindicesfile.close()
wordsfile.close()
seedwordsfile.close()
configfile.close()


