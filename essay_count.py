import liwc
import all_features
import csv
import re
from nltk.tokenize import word_tokenize
from wordsegment import segment

essay_data_file_path = "Essays data/essays.csv"
essay_data_output_path = "Essays data/essays_updated.csv"
classification_data_path = "Essays data/classification_data.csv"			
personality_categories = ["cEXT","cNEU","cAGR","cCON","cOPN"]			
DEBUG = False

from enchant.tokenize import get_tokenizer, HTMLChunker
def custom_word_tokenize(text):
	tokenizer = get_tokenizer("en_US")
	words = []
	for w in tokenizer(text):
		words.append(w[0])
	return words

def compute_scores_for_essays(essay, liwc_categories, liwc_trie):
	liwc_scores = dict()
	for category in liwc_categories:
		liwc_scores[category] = 0

	# Segment the words Present in the essay
	words_in_essay = custom_word_tokenize(essay)
	# print (essay)
	# words_in_essay = segment(essay)
	# Traverse the text word by word and count the words in each category
	if DEBUG:
		print(words_in_essay)
	for word in words_in_essay:
		# check if word prefix present in trie
		value = liwc_trie.longest_prefix(word)
		if value[0] is None:
			continue
		elif value[0] == word:
			# exact match thus increase counts
			if value[1][0] == "*":			
				for i in range(1,len(value[1])):
					liwc_scores[value[1][i]] += 1
			else:
				for category in value[1]:
					liwc_scores[category] += 1
		elif value[1][0] == "*":
			# star match thus increase counts
			for i in range(1,len(value[1])):
				liwc_scores[value[1][i]] += 1
	
	scores = []
	number_words = len(words_in_essay)
	for category in liwc_categories:
		scores.append(liwc_scores[category]/number_words)
	return scores

def create_classification_data(all_data, all_feature_labels):
	dataset_rows = []
	with open(classification_data_path, 'w') as csvoutput:
		writer = csv.writer(csvoutput)
		attribute_list = personality_categories + all_feature_labels
		l = len(attribute_list)
		for row in all_data:
			r = row[2:]
			if len(r)!=l:
				print("len not equal ",(len(r) - l))
			else:
				dataset_rows.append(r)
		writer.writerows(dataset_rows)

def generate_scored_essay_data(text):
	liwc_categories = liwc.get_list_of_liwc_categories()
	liwc_trie = liwc.create_trie_data_structure()
	
	feature_labels = all_features.get_all_feature_labels()

	# head_row = []
	# iteration = 0
	# with open(essay_data_file_path, 'r', encoding='utf-8') as csvinput:
	# 	with open(essay_data_output_path, 'w') as csvoutput:
	# 		writer = csv.writer(csvoutput)
	# 		reader = csv.reader(csvinput)
	# 		print("Printing Here!!")
	# 		print(reader)
	# 		head_row = next(reader)
	all_data = []
	head_row.extend(liwc_categories)
	head_row.extend(feature_labels)
	# all_data.append(head_row)
			# for row in reader:
				# compute LIWC Counts for individual categories
	scores = compute_scores_for_essays(text, liwc_categories, liwc_trie)
	features = all_features.get_all_features(text)
	dummy_row = row
	dummy_row.extend(scores)
	dummy_row.extend(features)
	all_data.append(dummy_row)
	# if DEBUG:
		# print(dummy_row)
	print("essay", iteration)
	iteration += 1
	all_feature_labels = []
	all_feature_labels.extend(liwc_categories)
	all_feature_labels.extend(feature_labels)
	create_classification_data(all_data, all_feature_labels)
	return all_data
	# writer.writerows(all_data)

def check_word_tokenizer():
	liwc_categories = liwc.get_list_of_liwc_categories()
	liwc_trie = liwc.create_trie_data_structure()
	print(liwc_categories)
	with open(essay_data_file_path, 'r', encoding='utf-8') as csvinput:
		reader = csv.reader(csvinput)
		head_row = next(reader)
		for row in reader:
			text = row[1]
			print(custom_word_tokenize(text))
			scores = compute_scores_for_essays(text, liwc_categories, liwc_trie)
			
			idx = 0
			for category in liwc_categories:
				print(category,scores[idx])
				idx+=1
			sleep(10)

def check_pos_tagging():
	with open(essay_data_file_path, 'r', encoding='utf-8') as csvinput:
		reader = csv.reader(csvinput)
		head_row = next(reader)
		for row in reader:
			text = row[1]
			words_custom = custom_word_tokenize(text)
			words_nltk = nltk.word_tokenize(text)
			pos_tag_custom = nltk.pos_tag(words_custom)
			print(words_nltk)
			print(pos_tag_custom)
			sleep(10)


def main(text = None):
	if text is None:
		return
	all_features.init()
	print generate_scored_essay_data(text)
	# check_word_tokenizer()
	# check_pos_tagging()

if __name__ == '__main__':
	main("I want to sleep and play all day")