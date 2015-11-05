import os

path = "/home/ashu/nlp_data/parsed_data"
question_title_line = 2
question_text_line = 5
question_description_line = 8
answer_line = 20

corpus = {}

from enchant.tokenize import get_tokenizer, HTMLChunker, URLFilter, WikiWordFilter
def custom_word_tokenize(text):
    chunkers = [HTMLChunker]
    filters = [URLFilter,WikiWordFilter]
    tokenizer = get_tokenizer("en_US",chunkers,filters)
    words = []
    for w in tokenizer(text):
        words.append(w[0])
    return words

def add_words(words):
    global corpus
    for word in words:
        if word in corpus:
            corpus[word] += 1
        else:
            corpus[word] = 1

def add_words_from_corpus_file():
    global corpus
    filename = "corpus.txt"
    with open(os.path.join(path,filename), 'r') as f:
        contents = f.readlines()
        index = 0
        for line in contents:
            print(index,len(corpus))
            index+=1
            if line != "None\n" and line != "&&&&&&&&&&&&\n":
                add_words(custom_word_tokenize(line))

def add_words_from_file(filename):
    # filename = "Zachary-Reiss-Davis_Why isn't there a Salesforce plug-in for Gmail?.txt"

    with open(os.path.join(path,filename), 'r') as f:
        contents = f.readlines()
        print(contents)
        # add_words(custom_word_tokenize(contents[question_title_line]))
        # add_words(custom_word_tokenize(contents[question_text_line]))
        # add_words(custom_word_tokenize(contents[question_description_line]))
        if answer_line != "None\n":
            add_words(custom_word_tokenize(contents[answer_line]))

import operator
def save_words():
    f = open("word_frequencies.txt","w")
    for word in sorted(corpus.items(), key=operator.itemgetter(1), reverse=True):
        print(word)
        f.write(str(word) + "\n")
    f.close()

import timeit

def main():
    # Check every file and extract answer words from it.
    print("Started")

    start = timeit.default_timer()

    for filename in os.listdir(path):
        print(filename) 
        #Your statements here
        stop = timeit.default_timer()
        print(stop - start)
        sleep(10)
        add_words_from_file(filename)

if __name__ == '__main__':
    # main()
    add_words_from_corpus_file()
    save_words()

