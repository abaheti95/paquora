import liwc
import quora_count
import all_features
import csv
from sys import argv

if __name__ == '__main__':
	f = open("sample.txt",'r',encoding="utf-8")
	text  = f.read()
	f.close()
	all_features.init()
	liwc_categories = liwc.get_list_of_liwc_categories()
	feature_labels = all_features.get_all_feature_labels()
	liwc_categories.extend(feature_labels)
	liwc_categories.append(argv[1])
	feature_vector = quora_count.get_feature_vector(text)
	feature_vector.append("?")
	# print(liwc_categories)
	# print(feature_vector)	
	with open(argv[1] + "test_data.csv", 'a') as csvoutput:
		writer = csv.writer(csvoutput)

		all_data = []
		# all_data.append(liwc_categories)
		all_data.append(feature_vector)
		writer.writerows(all_data)


