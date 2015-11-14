import csv
import numpy
import math
from sklearn import svm, cross_validation, naive_bayes, linear_model, ensemble

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

X = numpy.ndarray(shape = (len(examples), len(features)), dtype = float)
for i in range(0, len(examples)):
	for j in range(0, len(features)):
		X[i][j] = examples[i][j]

svmclassifier = svm.SVC()
# smoclassifier = svm.LinearSVC()
logisticclassifier = linear_model.LogisticRegression(C = math.exp(8), max_iter = 100000)
# logisticclassifier2 = linear_model.LogisticRegressionCV(Cs = [math.exp(8)], max_iter = 100000)
adaboostclassifier = ensemble.AdaBoostClassifier()
randomforestclassifier = ensemble.RandomForestClassifier(n_estimators = 100, random_state = 1)


for trait in range(0,5):
	Y = numpy.ndarray(shape = len(examples)	, dtype = float)
	if trait == 0: 
		for i in range(0, len(examples)):
			Y[i] = classEXT[i]
		print "Extraversion"
	elif trait == 1:
		for i in range(0, len(examples)):
			Y[i] = classEXT[i]
		print "Neuroticism"
	elif trait == 2:
		for i in range(0, len(examples)):
			Y[i] = classEXT[i]
		print "Agreeableness"
	elif trait == 3:
		for i in range(0, len(examples)):
			Y[i] = classEXT[i]
		print "Conscientiousness"
	else:
		for i in range(0, len(examples)):
			Y[i] = classEXT[i]
		print "Openness"
	# print "\t SVM = ",
	# scores = cross_validation.cross_val_score(svmclassifier, X, Y, cv = 10)
	# print scores.mean()
	# # print "\t SMO = ",
	# # scores = cross_validation.cross_val_score(smoclassifier, X, Y, cv = 10)
	# # print scores.mean()
	# print "\t Logistic Regression = ",
	# scores = cross_validation.cross_val_score(logisticclassifier, X, Y, cv = 10)
	# print scores.mean()
	# # print "\t Logistic Regression CV = ",
	# # scores = cross_validation.cross_val_score(logisticclassifier2, X, Y, cv = 10)
	# # print scores.mean()
	# print "\t AdaBoost Classification = ",
	# scores = cross_validation.cross_val_score(adaboostclassifier, X, Y, cv = 10)
	# print scores.mean()
	print "\t Random Forest Classification = ",
	scores = cross_validation.cross_val_score(randomforestclassifier, X, Y, cv = 10)
	print scores.mean()








