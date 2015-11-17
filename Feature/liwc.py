import mysql.connector
from mysql.connector import IntegrityError
from trie import StringTrie

DEBUG = False
def create_trie_data_structure():
	# open database
	liwc_db = mysql.connector.connect(host="localhost",user="nlp",password="nlppassword",database="nlp")
	cursor = liwc_db.cursor()
	t = StringTrie();
	
	cursor.execute("SELECT * FROM LIWC")
	liwc_data_list = cursor.fetchall()
	# generating Trie data structure
	if DEBUG:
		print("Creating Data Structure")
	for (Word, Type) in liwc_data_list:
		starString = False
		if Word.find('*') == -1:
			starString = False
		else:
			starString = True
		withoutStar = Word.replace("*","")
		if DEBUG:
			print(withoutStar," ",Word)
			print(Type)
		if t.has_node(withoutStar):
			dummy_list = t[withoutStar]
			dummy_list.append(Type)
			t.setdefault(withoutStar,dummy_list)
		else:
			dummy_list = list()
			if starString:
				dummy_list.append("*")
			dummy_list.append(Type)
			t.setdefault(withoutStar,dummy_list)
		if DEBUG:
			print("Print the value just added : ")
			print(t[withoutStar])
	liwc_db.close()
	return t

def create_liwc_dict():
	# open database
	liwc_db = mysql.connector.connect(host="localhost",user="nlp",password="nlppassword",database="nlp")
	cursor = liwc_db.cursor()
	
	cursor.execute("SELECT * FROM LIWC")
	liwc_data_list = cursor.fetchall()
	# generating Trie data structure
	t = {}
	if DEBUG:
		print("Creating Data Structure")
	for (Word, Type) in liwc_data_list:
		starString = False
		if Word.find('*') == -1:
			starString = False
		else:
			starString = True
		withoutStar = Word.replace("*","")
		if DEBUG:
			print(withoutStar," ",Word)
			print(Type)
		if withoutStar in t:
			dummy_list = t[withoutStar]
			dummy_list.append(Type)
			t[withoutStar] = dummy_list
		else:
			dummy_list = list()
			if starString:
				dummy_list.append("*")
			dummy_list.append(Type)
			t[withoutStar] = dummy_list
		if DEBUG:
			print("Print the value just added : ")
			print(t[withoutStar])
	liwc_db.close()
	return t

def get_list_of_liwc_categories():
	# open database
	liwc_db = mysql.connector.connect(host="localhost",user="nlp",password="nlppassword",database="nlp")
	cursor = liwc_db.cursor()

	cursor.execute("SELECT DISTINCT type FROM LIWC")

	liwc_categories = []

	for Type in cursor:
		liwc_categories.append(Type[0])

	liwc_db.close()
	return liwc_categories

def get_tag_words_dict():
	# open database
	liwc_db = mysql.connector.connect(host="localhost",user="nlp",password="nlppassword",database="nlp")
	cursor = liwc_db.cursor()

	cursor.execute("SELECT * FROM LIWC_Expanded")
	liwc_data_list = cursor.fetchall()
	# generating Trie data structure
	t = {}
	if DEBUG:
		print("Creating Data Structure")
	for (Word, Tag) in liwc_data_list:
		if Tag in t:
			t[Tag].append(Word)
		else:
			t[Tag] = [Word]
	liwc_db.close()
	return t

def save_expanded_liwc(liwc_words):
	# takes input of tag:words dict
	liwc_db = mysql.connector.connect(host="localhost",user="nlp",password="nlppassword",database="nlp")
	cursor = liwc_db.cursor()

	add_word = ("INSERT INTO LIWC_Expanded (word,type) VALUES (%s, %s)")
	for tag in liwc_words.keys():
		for word in liwc_words[tag]:
			data_tuple = (word, tag)
			cursor.execute(add_word, data_tuple)

	liwc_db.commit()

	cursor.close()
	liwc_db.close()

def save_new_expanded_liwc(liwc_words):
	# takes input of tag:words dict
	liwc_db = mysql.connector.connect(host="localhost",user="nlp",password="nlppassword",database="nlp")
	cursor = liwc_db.cursor()

	add_word = ("INSERT INTO LIWC_New_Expanded (word,type) VALUES (%s, %s)")
	for tag in liwc_words.keys():
		for word in liwc_words[tag]:
			data_tuple = (word, tag)
			try:
				cursor.execute(add_word, data_tuple)
			except IntegrityError as e:
				print("duplicate entry",word,tag)

	liwc_db.commit()

	cursor.close()
	liwc_db.close()

def test():
	liwc_trie = create_trie_data_structure()
	if DEBUG:
		print("Printing Trie Results")
		for key in liwc_trie.keys():
		 	print(key)
		print("Total Number of keys in Trie = " + str(len(liwc_trie.keys())))

	liwc_categories = get_list_of_liwc_categories()
	if DEBUG:
		print("Printing LIWC categories here :")
		print(liwc_categories)
		print("Number of categories = " + str(len(liwc_categories)))

