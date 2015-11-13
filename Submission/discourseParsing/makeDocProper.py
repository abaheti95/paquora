from sys import argv
import nltk
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import csv

"""
There are two functions in this feature, one takes direct text as input
The other one will take a file name as input and return the words per sentence
The output you will get is: (AverageNumberOfWordsPerSentence, PerSentenceWordCountList[])
I am taking not taking punctuations as words and hence removed it. If you need to migrate to Python 3, then uncomment the line mentioned.
"""
abbreviations = {'dr.': 'doctor', 'mr.': 'mister', 'bro.': 'brother', 'bro': 'brother', 'mrs.': 'mistress', 'ms.': 'miss', 'jr.': 'junior', 'sr.': 'senior',
                 'i.e.': 'for example', 'e.g.': 'for example', 'vs.': 'versus'}
terminators = ['.', '!', '?']
wrappers = ['"', "'", ')', ']', '}']
def find_sentences(paragraph):
   end = True
   sentences = []
   while end > -1:
       end = find_sentence_end(paragraph)
       if end > -1:
           sentences.append(paragraph[end:].strip())
           paragraph = paragraph[:end]
   sentences.append(paragraph)
   sentences.reverse()
   return sentences


def find_sentence_end(paragraph):
    [possible_endings, contraction_locations] = [[], []]
    contractions = abbreviations.keys()
    sentence_terminators = terminators + [terminator + wrapper for wrapper in wrappers for terminator in terminators]
    for sentence_terminator in sentence_terminators:
        t_indices = list(find_all(paragraph, sentence_terminator))
        possible_endings.extend(([] if not len(t_indices) else [[i, len(sentence_terminator)] for i in t_indices]))
    for contraction in contractions:
        c_indices = list(find_all(paragraph, contraction))
        contraction_locations.extend(([] if not len(c_indices) else [i + len(contraction) for i in c_indices]))
    possible_endings = [pe for pe in possible_endings if pe[0] + pe[1] not in contraction_locations]
    if len(paragraph) in [pe[0] + pe[1] for pe in possible_endings]:
        max_end_start = max([pe[0] for pe in possible_endings])
        possible_endings = [pe for pe in possible_endings if pe[0] != max_end_start]
    possible_endings = [pe[0] + pe[1] for pe in possible_endings if sum(pe) > len(paragraph) or (sum(pe) < len(paragraph) and paragraph[sum(pe)] == ' ')]
    end = (-1 if not len(possible_endings) else max(possible_endings))
    return end


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)

def make_good_sentence(data):
    splat = data.split("\n\n")
    text = ""
    for paragraph in splat:
        paragraph = paragraph.strip()
        paragraph = paragraph.replace('."','".')
        sentences = find_sentences(paragraph)

        for i in range(0,len(sentences)-1):
            print sentences[i]
            text = text + sentences[i]+ "<s>\n"

        text = text + sentences[len(sentences)-1]
        text=text+"<p>"+"\n"

    return text

if __name__ == '__main__':

    with open('essays_updated.csv', 'rb') as csvfile:
        rows= csv.reader(csvfile)
        i=0
        for row in rows:
          if(i==0):
            #first line is csv header
            i=i+1
            continue
          data=row[1]
          text = make_good_sentence(data)
          with open("tagged_sentences/essay_"+str(i)+".txt","w") as fr:
              fr.write(text)
          i=i+1
    # f = open(argv[1], 'r')
    # data = f.read()
    
