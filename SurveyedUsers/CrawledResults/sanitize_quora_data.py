import csv
import re
import codecs

quora_data_file_path = "quora_user_answer.csv"
quora_data_output_path = "quora_user_answer_sanitized.csv"

def main():
	counter = 0
	with open(quora_data_file_path, 'r', encoding='utf-8') as csvinput:
		with open(quora_data_output_path, 'w') as csvoutput:
			writer = csv.writer(csvoutput)
			reader = csv.reader(csvinput)
			all_data = []
			for index,row in enumerate(reader):
				# print(row)
				# print(index)
				if len(row) < 2:
					continue
				text = row[1]
				if not text or text.isspace():
					counter += 1
				else:
					all_data.append(row)
			writer.writerows(all_data)

	print("Counter", counter)

	
if __name__ == '__main__':
	main()
