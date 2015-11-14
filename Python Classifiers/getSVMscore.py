import csv
import numpy
import math
from sklearn import svm

csvfile = open("../Essays data/classification_data.csv")
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

sample = numpy.ndarray(shape = len(features), dtype = float)
sample = X[-1]
print svmclassifierEXT.predict(sample), YEXT[-1]
print svmclassifierNEU.predict(sample), YNEU[-1]
print svmclassifierAGR.predict(sample), YAGR[-1]
print svmclassifierCON.predict(sample), YCON[-1]
print svmclassifierOPN.predict(sample), YOPN[-1]