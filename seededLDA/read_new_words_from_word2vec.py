import liwc

word2vec_file = "word2vec_words.txt"

def main():
	new_words = {}
	new_words_count = 0
	with open(word2vec_file) as f:
		content = f.readlines()
		for i in range(0,len(content),2):
			if i+1 == len(content):
				break
			words = content[i+1].split(",")
			# remove full stop and spaces
			sanitized_words = list(set([word.replace(".","").strip() for word in words]))
			# remove empty words
			non_empty_sanitized_words = list(filter(None, sanitized_words))
			tag = content[i].strip()
			new_words[tag] = non_empty_sanitized_words
			print(tag, non_empty_sanitized_words)
			new_words_count += len(non_empty_sanitized_words)

	print(new_words_count)

	"""liwc_words = liwc.get_tag_words_dict()
	# Expand LIWC
	for tag in new_words.keys():
		liwc_words[tag].extend(new_words[tag])
		liwc_words[tag] = list(set(liwc_words[tag]))
	# Save expanded LIWC
	liwc.save_expanded_liwc(liwc_words)"""
	


if __name__ == '__main__':
	main()