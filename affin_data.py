import csv
import re
def rate_essays(essay):
	words_in_essay = re.compile("[^A-Za-z]").split(essay)
	score = 0
	count = 0
	for word in words_in_essay:
		if word in affine_dict:
			score = score + affine_dict[word]
			count = count + 1
	average_score = 0
	if count != 0:
		average_score = score/count
	return average_score


def generate_scored_essay_data():
	head_row = []
	write_rows = []
	with open(essay_data_file_path, 'rb') as csvinput:
		with open(essay_data_output_path, 'w') as csvoutput:
			writer = csv.writer(csvoutput)
			reader = csv.reader(csvinput)
			head_row = next(reader)
			cur_row = head_row[2:]
			cur_row.append("Score")
			write_rows.append(cur_row)
			for row in reader:
				# compute LIWC Counts for individual categories
				score = rate_essays(row[1])
				cur_row = row[2:] 
				cur_row.append(str(score))
				write_rows.append(cur_row)
			writer.writerows(write_rows)


affin_words_path = "AFINN/AFINN-111.txt"
essay_data_output_path = "Essays data/affin_data.csv"
essay_data_file_path = "Essays data/essays.csv"
affine_file = open(affin_words_path, "r")
affine_dict = dict()
for line in affine_file:
	words = line.split()
	word = words[0].strip()
	score = int(words[-1].strip())
	affine_dict[word] = score

generate_scored_essay_data()
