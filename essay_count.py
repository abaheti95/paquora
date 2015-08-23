exec(open("liwc.py").read())
import csv
import re

essay_data_file_path = "Essays data/essays.csv"
essay_data_output_path = "Essays data/essays_updated.csv"

DEBUG = False

def compute_scores_for_essays(essay, liwc_categories, liwc_trie):
	liwc_scores = dict()
	for category in liwc_categories:
		liwc_scores[category] = 0

	# Traverse the text word by word and count the words in each category
	essay = essay.replace("\\'", "")
	words_in_essay = re.compile("[^A-Za-z]").split(essay)
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
	for key, value in liwc_scores.iteritems():
		scores.append(value)
	return scores


def generate_scored_essay_data():
	liwc_categories = get_list_of_liwc_categories()
	liwc_trie = create_trie_data_structure()
	
	head_row = []
	with open(essay_data_file_path, 'rb') as csvinput:
		with open(essay_data_output_path, 'w') as csvoutput:
			writer = csv.writer(csvoutput)
			reader = csv.reader(csvinput)
			head_row = next(reader)
			all_data = []
			head_row.extend(liwc_categories)
			all_data.append(head_row)
			for row in reader:
				# compute LIWC Counts for individual categories
				scores = compute_scores_for_essays(row[1], liwc_categories, liwc_trie)
				dummy_row = row
				dummy_row.extend(scores)
				all_data.append(dummy_row)
				if DEBUG:
					print(dummy_row)
			
			writer.writerows(all_data)

def main():
	generate_scored_essay_data()

if __name__ == '__main__':
	main()