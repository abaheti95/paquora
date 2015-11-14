__author__ = 'nishkarsh'

'''
Created on Feb 19, 2013

@author: Vanessa Wei Feng
'''
from nltk.tree import *
import collections

from string import *
import re
from yappsrt import *
import csv

relations = {}
relations["Antithesis"]= 0
relations["Attribution"]=0
relations["Background"]= 0
relations["Backgroundrelations"]= 0
relations["Cause"]= 0
relations["Circumstance"]= 0
relations["Comparison"]= 0
relations["Concession"]= 0
relations["Condition"]= 0
relations["Contrast"]= 0
relations["Elaboration"]= 0
relations["Enablement"]= 0
relations["Evaluation"]= 0
relations["Evidence"]= 0
relations["Explanation"]= 0
relations["Joint"]= 0
relations["Justify"]= 0
relations["List"]= 0
relations["Manner-Means"]= 0
relations["Motivation"]= 0
relations["Non-volitional Cause"]= 0
relations["Non-volitional Result"]= 0
relations["Otherwise (anti conditional)"]= 0
relations["Restatement"]= 0
relations["Sequence"]= 0
relations["Solutionhood"]= 0
relations["Summary"]= 0
relations["Temporal"]= 0
relations["Topic-Change"]= 0
relations["Topic-Comment"]= 0
relations["Volitional Cause"]= 0
relations["Volitional Result"]= 0
relations["same-unit"]= 0
relations["span"]= 0
relations["textual-organization"] = 0





class TreebankScanner(Scanner):
    patterns = [
        ('r"\\)"', re.compile('\\)')),
        ('r"\\("', re.compile('\\(')),
        ('"_!"', re.compile('_!')),
        ('\\s+', re.compile('\\s+')),
        ('//TT_ERR', re.compile('//TT_ERR')),
        ('NUM', re.compile('[0-9]+')),
        ('ID', re.compile('[-+*/!@$%^&=.a-zA-Z0-9]+')),
        ('STR', re.compile('(.)+_!')),
    ]
    def __init__(self, str):
        Scanner.__init__(self,None,['\\s+', '//TT_ERR'],str)

class Treebank(Parser):
    def expr(self):
        _token_ = self._peek('"_!"', 'ID', 'NUM', 'r"\\("')
        if _token_ == '"_!"':
            self._scan('"_!"')
            STR = self._scan('STR')
            return STR[0:-2]
        elif _token_ == 'ID':
            ID = self._scan('ID')
            return ID
        elif _token_ == 'NUM':
            NUM = self._scan('NUM')
            return atoi(NUM)
        else:# == 'r"\\("'
            self._scan('r"\\("')
            ID = self._scan('ID')
            e = []
            while self._peek('r"\\)"', '"_!"', 'ID', 'NUM', 'r"\\("') != 'r"\\)"':
                expr = self.expr()
                e.append(expr)
            self._scan('r"\\)"')
            return ParentedTree(ID, e)


def parse(rule, text):
    P = Treebank(TreebankScanner(text))
    return wrap_error_reporter(P, rule)

def parse(text):
    P = Treebank(TreebankScanner(text))
    return wrap_error_reporter(P, 'expr')

def extractNucleusText(P):
    x=""
    for subtree in P.subtrees(lambda t: t.node == 'Nucleus'):
        # if subtree.label()=='Nucleus':
            x = subtree
            break
    text = ""
    for subtree in x.subtrees():
        if subtree.node=="text":
            # print subtree.leaves()
            # print subtree[0]
            st = subtree[0].replace("_!","")
            st = st.replace("!_","")
            st = st.replace("<s>","")
            text = text + " " + st
    return text.strip()

def findAllRelations(P):
    relation = {}
    relation["Antithesis"]= 0
    relation["Attribution"]=0
    relation["Background"]= 0
    relation["Backgroundrelations"]= 0
    relation["Cause"]= 0
    relation["Circumstance"]= 0
    relation["Comparison"]= 0
    relation["Concession"]= 0
    relation["Condition"]= 0
    relation["Contrast"]= 0
    relation["Elaboration"]= 0
    relation["Enablement"]= 0
    relation["Evaluation"]= 0
    relation["Evidence"]= 0
    relation["Explanation"]= 0
    relation["Joint"]= 0
    relation["Justify"]= 0
    relation["List"]= 0
    relation["Manner-Means"]= 0
    relation["Motivation"]= 0
    relation["Non-volitional Cause"]= 0
    relation["Non-volitional Result"]= 0
    relation["Otherwise (anti conditional)"]= 0
    relation["Restatement"]= 0
    relation["Sequence"]= 0
    relation["Solutionhood"]= 0
    relation["Summary"]= 0
    relation["Temporal"]= 0
    relation["Topic-Change"]= 0
    relation["Topic-Comment"]= 0
    relation["Volitional Cause"]= 0
    relation["Volitional Result"]= 0
    relation["same-unit"]= 0
    relation["span"]= 0
    relation["textual-organization"] = 0

    x=""
    height = 0
    for subtree in P.subtrees():
        if subtree.node=='rel2par':
            for leave in subtree.leaves():
                if leave in relation:
                    relation[leave]=relation[leave]+1
                else:
                    relation[leave]=1
                # print leave
    od = collections.OrderedDict(sorted(relation.items()))
    return od
    # for key in od:
    #     print key,d[key]

if __name__=='__main__':
    print 'Testing'
    with open("discourse_essay_data.csv","a") as f:
        a = csv.writer(f, delimiter=',')
        row = []
        row.append("Essay_Number")
        row.append("Nucleus Text")
        for key in collections.OrderedDict(sorted(relations.items())):
            row.append(key)
        a.writerow(row)
    f = open("result_of_dis_list.txt","r")
    lines = f.read().splitlines()
    for line in lines:
        print "getting "+line
        disTreeFile = open("tagged_sentences/"+line,"r")

        str = disTreeFile.read()
        P = parse(str)

        nucleus=extractNucleusText(P)
        relation=findAllRelations(P)

        with open("discourse_essay_data.csv","a") as fd:
            a = csv.writer(fd, delimiter=',')
            row = []
            row.append((line.split("_")[1]).split(".")[0])
            row.append(nucleus)
            for key in relation:
                row.append(relation[key])
            a.writerow(row)
        print "\n\n\n"
        # print extractSatelliteText(P)
    # with open("Nucleus_data.txt","wa") as f:
    #     f.write(text)
    # od = collections.OrderedDict(sorted(relations.items()))            
    # for key in od:
    #     print key,od[key]