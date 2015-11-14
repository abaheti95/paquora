import csv
import re

quora_data_file_path = "quora_user_scores.csv"
quora_data_output_path = "quora_user_personalities.csv"

def main():
	with open(quora_data_file_path, 'r', encoding='utf-8') as csvinput:
		with open(quora_data_output_path, 'w') as csvoutput:
			writer = csv.writer(csvoutput)
			reader = csv.reader(csvinput)

			labels = ["Name","Username","O","C","E","A","N"]
			all_data = [labels]
			for index,row in enumerate(reader):
				# print(row)
				print(index)
				if len(row) < 7:
					continue
				for i in range(2,7):
					if int(row[i]) < 5:
						row[i] = "low"
					elif int(row[i]) > 6:
						row[i] = "high"
					else:
						row[i] = "mid"
				all_data.append(row)

			writer.writerows(all_data)



if __name__ == '__main__':
	main()