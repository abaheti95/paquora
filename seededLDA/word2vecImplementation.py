import gensim
import logging
import os
import cython
import liwc
import mysql
import mysql.connector
import re

import fnmatch

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

if __name__ == '__main__':
    sentences = MySentences("corpus")
    sentencesQuora = MySentences("sentencesQuora")
    # quoramodel = gensim.models.Word2Vec(sentencesQuora,min_count=10,size=200,workers=4)
    quoraModel  = gensim.models.Word2Vec.load('myModel')
    # quoramodel.save('myModel')
    wikiModel  = gensim.models.Word2Vec.load('myModel2')

    vocab = quoraModel.vocab
    liwc_tags = liwc.get_list_of_liwc_categories()
    liwc_trie = liwc.create_trie_data_structure()
    print liwc_tags
    tag_dict = {}
    new_tag_dict = {}

    tag_dict = liwc.get_tag_words_dict()
    for tag in liwc_tags:
        print "------------------",tag,"----------------------------------------"
        new_tag_dict[tag]=set()
        word_list = tag_dict[tag]
        for word in word_list:
            # handle the conditions when word contains *
            print word
            wordlist = []
            wordlist.append(word)
            if (word.endswith('*')):
                wordlist = fnmatch.filter(vocab,word)
                print wordlist
            for w in wordlist:
                try:
                    w = re.sub('[^a-zA-Z0-9-_*.]', '', w)
                    word_tuple = quoraModel.most_similar(positive=[w],topn=30)
                    for (word,similarity) in word_tuple:
                        if similarity>0.7:
                            try:
                                sim = wikiModel.similarity(w,word)
                                if(sim>0.7):
                                    new_tag_dict[tag].add(w.lower())
                            except:
                                print "No vacabulary in billion words for",w

                except:
                    print "No vacabulary for word: ",w

    new_word_tag_dict={}
    for tag in liwc_tags:
        new_word_tag_dict[tag]=set()
        words = new_tag_dict[tag]
        for word in words:
            # check if word prefix present in trie
            # preprocess word before checking
            word = word.lower()
            # Strip special characters

            value = liwc_trie.longest_prefix(word.lower())
            # Either the word in not present
            # Or the prefix is present but it is not a star word
            # Or the prefix is present and its a star word but tag is not present
            # Or it is whole word and tag is not present
            if value[0] is None:
                new_word_tag_dict[tag].add(word)
            elif tag not in value[1]:
                new_word_tag_dict[tag].add(word)
            elif value[0] is not word and '*' not in value[1]:
                new_word_tag_dict[tag].add(word)

    f = open("word2vec_words.txt","w")
    for tag in liwc_tags:
        f.write("\n-------------------------------")
        f.write("Tag is "+tag)
        f.write("-------------------------------\n")
        for word in new_word_tag_dict[tag]:
            f.write(word)
            f.write(" , ")