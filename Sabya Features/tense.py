import csv
from nltk import word_tokenize, pos_tag
from PlotFeatures import Plotfeatures
import numpy as np
import matplotlib.pyplot as plt

past_tense_data = []
present_tense_data = []
with open("essays.csv", "rU") as f:
	reader = csv.reader(f)
	head_row = next(reader)
	essay_id = 1
	for row in reader:
		essay = row[1]
		class_label = row[6]
		if class_label == "y":
			class_number = 0
		else:
			class_number = 1
		text = word_tokenize(essay)
		pos_tagged_text = pos_tag(text)
		VB = []
		VBD = []
		VBG = []
		VBN = []
		VBP = []
		VBZ = []
		Others = []
		for (word, tag) in pos_tagged_text:
			if tag == "VB":
				VB.append(word)
			elif tag == "VBD":
				VBD.append(word)
			elif tag == "VBG":
				VBG.append(word)
			elif tag == "VBN":
				VBN.append(word)
			elif tag == "VBP":
				VBP.append(word)
			elif tag == "VBZ":
				VBZ.append(word)
			elif tag.find("VB") != -1:
				Others.append(word)
		number_past_tense = len(VBD) + len(VBP)
		number_present_tense = len(VBG)
		past_tense_data.append((essay_id, number_past_tense, class_number))
		present_tense_data.append((essay_id, number_present_tense, class_number))
		print essay_id,
		essay_id += 1

f = open("past_tense", "w")
for (essay_id, number_past_tense, class_number) in past_tense_data:
	f.write(str(essay_id) + " " + str(number_past_tense) + " " + str(class_number))
	f.write("\n")
f.close()
f = open("present_tense", "w")
for (essay_id, number_present_tense, class_number) in present_tense_data:
	f.write(str(essay_id) + " " + str(number_present_tense) + " " + str(class_number))
	f.write("\n")
f.close()
# past_tense_plot = Plotfeatures(past_tense_data, "past_tense")
# past_tense_plot.plot_data()
# past_tense_plot.save_fig()

# present_tense_plot = Plotfeatures(present_tense_data, "present_tense")
# present_tense_plot.plot_data()
# present_tense_plot.save_fig()
