import liwc
import all_features
import csv
import re
from nltk.tokenize import word_tokenize
from wordsegment import segment

essay_data_file_path = "../Essays data/essays.csv"
essay_data_output_path = "../Essays data/essays_updated.csv"
classification_data_path = "../Essays data/classification_data.csv"
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

	head_row = []
	iteration = 0
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
	dummy_row = []
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
	# create_classification_data(all_data, all_feature_labels)
	return all_data
	# writer.writerows(all_data)

def check_word_tokenizer():
	liwc_categories = liwc.get_list_of_liwc_categories()
	liwc_trie = liwc.create_trie_data_structure()
	print(liwc_categories)
	with open(essay_data_file_path, 'r') as csvinput:
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
	with open(essay_data_file_path, 'r') as csvinput:
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
	return generate_scored_essay_data(text)
	# check_word_tokenizer()
	# check_pos_tagging()

# if __name__ == '__main__':
# 	main("  I don't want to be in ROTC, but I have to strive for a scholarship. My parents can't afford to send me through all four years in college. I need money!!  I hat ROTC. it's so stupid. Left face. Right Face. Bullshit. I don't want to be in the military. But to save my parents money I guess I'm going to have to put up with it. Oh well. Man I can't believe I slept  I mean overslept through Nursing. I was there for only the last fifteen minutes of class. That makes two classes that I missed. Chemistry Lab and now this. I have to make straight A's I have to. I must succeed. My parents worked hard to see that I do. Damn it. I would be perfectly happy living in a small apartment working as a waitress well may be not a waitress. May be a teacher . Anything . I don't care how much money I make. But I owe it tom my parents. I'm not going to be like my brother. Damn I need to buy some shoe polish and some brasso for ROTC. Gaw I hate ROTC. I'm already taking fifteen hours plus four more hours or is it 3? of ROTC. That is too much for a freakin freshman. At least to me it is. Man twelve more minutes to go. I hate my roommate. She's such a bitch. She's a pig too. She ate all of my peaches. I said she could have one not twenty. I'm tired of techno music. I like rap and r&b. They don't play that shit down here. I wish Sabrina would hurry up. I'm hungry. I'm so stressed. I need a break. Summer was too short. I miss Louis. I miss sex. I need sex. That'll relieve my stress. But I can't do that. It's against my morals. Yeah right. Why don't I have sex?  There are so many guys around here that would be more than willing to have sex with me. I'm so damn attractive. I'm like a magnet. I think that's the only thing really going for me. My looks. But that sure ain't going to last. I need to start concentrating on getting my mind fit instead of my body all the time. I wish I was as smart as other people. I want to be a pediatrician. No actually I want to be a veterinarian. But oh well. May be some other lifetime. Hopefully she or he would be more prepared than I was. I love Louis, but do I want to marry him. Will he be faithful to me. Does he really love me?  I love his son so much. Perrion. Perrion. I love Perrion. I wish I could see him. I love him more than his father. I would do anything for that little boy. Damn I hate the mother. I have never been jealous of anyone in my life, except for her. Shelly Malley. I hate her. No I don't hate anyone. I'm such a nice person. I couldn't hurt a soul. That night I could've pounded her ass, but I didn't. I have self control and I have maturity. But damn it would have felt so good just to break her face. I miss Leona. I can't believe she didn't want to spend any time with me when I came down to visit. That hurt so bad. I loved that girl. She was like a sister to me. What happened?  My loved ones are leaving me left and right. Soon daddy is going to pass away. No. I don't want you to daddy. I love you so much. Why can't god give some one else his pain and suffering. He doesn't deserve it god. Give it to fucking Charles Manson or that guy that killed that little girl in Killeen. But not my daddy. It's not fair. Okay 20 minutes passed. I'm done")