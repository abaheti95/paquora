from wordsegment import segment

def custom_word_tokenize(text):
	# First split the text by spaces
	possible_words = text.split()
	# Now use segment function from wordsegment library
	words = []
	for possible_word in possible_words:
		words.extend(segment(possible_word))
	return words

"""
Takes the list of words in the text as input and calculates the number of words of length greater than equal 6,7,8,9
:param words: List of strings which are actually words in the text without spaces
:returns: tuple of integer counts
"""
def pref_for_longer_words(words):
	count_6 = 0
	count_7 = 0
	count_8 = 0
	count_9 = 0
	for word in words:
		length = len(word)
		if length >= 6:
			count_6 +=  1
		if length >= 7:
			count_7 += 1
		if length >= 8:
			count_8 +=  1
		if length >= 9:
			count_9 += 1
	return count_6, count_7, count_8, count_9

"""
Takes the text and number of sentences as input and counts the number of punctuations in it.
:param text: Complete text. This text should not contain numbers and emojis
:param num_sentences: Number of sentences
:returns: number of punctuations used in the text 
"""
punctuations = ['.', '"',"'",'{','(','-','!','?',':']
def count_punctuations(text, num_sentences):
	dots = text.count('.')
	punct_count = 0
	for punctuation in punctuations:
		if punctuation == '.':
			punct_count += num_sentences
		elif punctuation == '"':
			punct_count += int(text.count(punctuation)/2)
		else:
			punct_count += int(text.count(punctuation))
	return punct_count
