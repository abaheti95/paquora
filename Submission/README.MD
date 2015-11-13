DISCOURSE PARSING
-----------------
Discourse Parsing Tool Used from this Site: http://www.cs.toronto.edu/~weifeng/software.html
It creates a RST Style discoure tree given a properly formatted input text.

In the folder Discourse Parsing Results, Discourse Tree holds the RST style tree of 2000 essays. In the csv file discourse_essay_data.csv, each essay's nucleus text, the relations present and the number of times that relation has occured is present.

makeDocProper.py : segments the given text into sentences and paragraphs in the format prescribed by the software.

runParser.py : uses the software's "parse" executable to parse all the essays in the file list given in the script and outputs the RST discourse tree.

findMainNucleus.py: Extracts the nucleus text and all the relations present in the text. Does the same for all the text files and outputs the result in a csv file.

SEEDED LDA
----------
LDA (Latent Dirichlet Allocation) is a topic model. It generates topic from a corpus of documents using word frequency from documents that is treated as a bag of words. Here we illustrate the steps employed while generating topics from our corpus and end by giving a brief description of how LDA works.

We used LDA to extend our list of Linguistic Inquiry and Word Count(LIWC) words. Our corpus consisted of documents that had the textual content of quora users’ answers. The number of documents equaled 2000. The number of LIWC words that were used to seed the LDA process is 4488 coming from 64 categories.

The packages involved are - gensim (LDA), pyenchant(Chunker and Tokeniser), numpy(seeded Matrix)
The steps involved are -
	1.	The quora answers are read into lists
	2.	Each document is processed - case folding, filtering html tags and links, extracting only english words
	3.	LIWC words are read
	4.	A dictionary is created from the answers and each document is converted into a document term matrix of word frequency
	5.	Collection frequency is calculated for each word
	6. 	The seed matrix is calculated. The number of topics equal 64 and the words in each topic equal the intersection of the LIWC words of 		that topic and the quora vocabulary created in step 4.
	7.	LDA is run. We use the parallel version to reduce time, employing 4 worker threads.
	8.	For each topic we set a threshold of 0.05 of probability and select the top 1000 words from each topic different from those already 		present in LIWC.

LDA assumes documents are produced from a mixture of topics. Those topics then generate words based on their probability distribution, in other words, LDA assumes a document is made from the following steps:

	1.	Determine the number of words in a document. Let’s say our document has 6 words.
	2.	Determine the mixture of topics in that document. 
	3.	Using each topic’s multinomial distribution, output words to fill the document’s word slots. 