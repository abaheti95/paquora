import csv
import numpy
import math
from sklearn import svm
from sklearn import cross_validation
import quora_count

def getscore(text):
	csvfile = open("../Essays data/classification_data.csv", "rb")
	csvreader = csv.reader(csvfile)
	header = csvreader.next()
	classEXT = []
	classNEU = []
	classAGR = []
	classCON = []
	classOPN = []
	examples = []
	features = []
	for feature in header[5:]:
		features.append(feature)
	for row in csvreader:
		if row[0] == 'y':
			classEXT.append(1)
		else:
			classEXT.append(0)

		if row[1] == 'y':
			classNEU.append(1)
		else:
			classNEU.append(0)

		if row[2] == 'y':
			classAGR.append(1)
		else:
			classAGR.append(0)

		if row[3] == 'y':
			classCON.append(1)
		else:
			classCON.append(0)

		if row[4] == 'y':
			classOPN.append(1)
		else:
			classOPN.append(0)

		example = []
		for value in row[5:]:
			example.append(value)
		examples.append(example)

	svmclassifierEXT = svm.SVC()
	svmclassifierNEU = svm.SVC()
	svmclassifierAGR = svm.SVC()
	svmclassifierCON = svm.SVC()
	svmclassifierOPN = svm.SVC()
	X = numpy.ndarray(shape = (len(examples), len(features)), dtype = float)
	for i in range(0, len(examples)):
		for j in range(0, len(features)):
			X[i][j] = examples[i][j]
	YEXT = numpy.ndarray(shape = len(examples)	, dtype = float)
	YNEU = numpy.ndarray(shape = len(examples)	, dtype = float)
	YAGR = numpy.ndarray(shape = len(examples)	, dtype = float)
	YCON = numpy.ndarray(shape = len(examples)	, dtype = float)
	YOPN = numpy.ndarray(shape = len(examples)	, dtype = float)

	for i in range(0, len(examples)):
				YEXT[i] = classEXT[i]
				YNEU[i] = classNEU[i]
				YAGR[i] = classAGR[i]
				YCON[i] = classCON[i]
				YOPN[i] = classOPN[i]

	svmclassifierEXT.fit(X, YEXT)
	svmclassifierNEU.fit(X, YNEU)
	svmclassifierAGR.fit(X, YAGR)
	svmclassifierCON.fit(X, YCON)
	svmclassifierOPN.fit(X, YOPN)

	# print cross_validation.cross_val_score(svmclassifierEXT, X, YEXT, cv=10).mean()
	# print cross_validation.cross_val_score(svmclassifierNEU, X, YNEU, cv=10).mean()
	# print cross_validation.cross_val_score(svmclassifierAGR, X, YAGR, cv=10).mean()
	# print cross_validation.cross_val_score(svmclassifierCON, X, YCON, cv=10).mean()
	# print cross_validation.cross_val_score(svmclassifierOPN, X, YOPN, cv=10).mean()

	sample = numpy.ndarray(shape = len(features), dtype = float)
	print(text)
	# feature_vector = essay_count.main(text)[0][5:]
	feature_vector = quora_count.get_feature_vector()
	# print feature_vector
	# print "yyyyyyyyyyyyyyyyyyyyy"
	for i in range(0, len(feature_vector)):
		sample[i] = feature_vector[i]
	A =  svmclassifierEXT.predict(sample)
	B =  svmclassifierNEU.predict(sample)
	C =  svmclassifierAGR.predict(sample)
	D =  svmclassifierCON.predict(sample)
	E =  svmclassifierOPN.predict(sample)
	return (A,B,C,D,E)

