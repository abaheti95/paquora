import liwc
import csv

pos_tag = "Posemo"
neg_tag = "Negemo"
func_tag = "Funct"
positive_words_file = "pos-neg/positive_words.csv"
negative_words_file = "pos-neg/negative_words.csv"
func_words_file = "func_words.csv"

def add_funct_words(liwc_words):
	func_words = []
	with open(func_words_file, 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for row in reader:
			func_words.append(row[0])

	existing_func_words = liwc_words[func_tag]
	all_func_words = list(set(func_words) | set(existing_func_words))
	liwc_words[func_tag] = all_func_words

def add_negative_words(liwc_words):
	neg_words = []
	with open(negative_words_file, 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for row in reader:
			neg_words.append(row[0])

	existing_neg_words = liwc_words[neg_tag]
	all_neg_words = list(set(neg_words) | set(existing_neg_words))
	liwc_words[neg_tag] = all_neg_words

def add_positive_words(liwc_words):
	pos_words = []
	with open(positive_words_file, 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for row in reader:
			pos_words.append(row[0])

	existing_pos_words = liwc_words[pos_tag]
	all_pos_words = list(set(pos_words) | set(existing_pos_words))
	liwc_words[pos_tag] = all_pos_words

def main():
	# get liwc words
	liwc_words = liwc.get_tag_words_dict()

	add_positive_words(liwc_words)
	print("Positive done")
	add_negative_words(liwc_words)
	print("Negative done")
	add_funct_words(liwc_words)
	print("Func done")

	liwc.save_new_expanded_liwc(liwc_words)


if __name__ == '__main__':
	main()
