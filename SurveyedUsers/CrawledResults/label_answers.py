import csv
import re
import codecs

quora_personalites_file_path = "quora_user_personalities.csv"
quora_answers_input_path = "quora_user_answer.csv"
quora_answers_label_output_path = "quora_answer_label200.csv"


from wordsegment import segment
from enchant.tokenize import get_tokenizer, HTMLChunker
def custom_word_tokenize(text):
	tokenizer = get_tokenizer("en_US")
	words = []
	for w in tokenizer(text):
		words.append(w[0])
	return words

def get_personalities_dict():
	user_personalities = dict()
	with open(quora_personalites_file_path, 'r', encoding='utf-8') as csvinput:
		reader = csv.reader(csvinput)

		# skip the head row
		head_row = next(reader)
		for index,row in enumerate(reader):
			# print(row)
			# print(index)
			if len(row) < 7:
				continue
			username = row[1].split("/")[-1]
			ocean = [row[2], row[3], row[4], row[5], row[6]]
			user_personalities[username] = ocean
	return user_personalities

def main():
	counter = 0
	user_personalities = get_personalities_dict()
	for username in user_personalities.keys():
		print(username,user_personalities[username])

	with open(quora_answers_input_path, 'r', encoding='utf-8') as csvinput:
		with open(quora_answers_label_output_path, 'w') as csvoutput:
			writer = csv.writer(csvoutput)
			reader = csv.reader(csvinput)
			head_row = next(reader)
			labels = ["username","text","O","C","E","A","N"]
			all_data = [labels]
			for index,row in enumerate(reader):
				# print(row)
				# print(index)
				if len(row) < 2:
					continue
				# check word count greater than 300
				# print(custom_word_tokenize(row[1]))
				if len(custom_word_tokenize(row[1])) < 200:
					continue
				print(index)
				ocean = user_personalities[row[0]]
				row.extend(ocean)
				all_data.append(row)
			writer.writerows(all_data)

	
if __name__ == '__main__':
	main()
