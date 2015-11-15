import mysql.connector
# import MySQLdb as mdb
from trie import StringTrie

DEBUG = False
def create_trie_data_structure():
	# open database
	liwc_db = mysql.connector.connect(host="localhost",user="nlp",password="nlppassword",database="nlp")
	cursor = liwc_db.cursor()
	t = StringTrie();
	
	cursor.execute("SELECT * FROM LIWC_New_Expanded")
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

