import MySQLdb
execfile("trie.py")

DEBUG = False
def create_trie_data_structure():
	# open database
	liwc_db = MySQLdb.connect("localhost","nlp","nlppassword","nlp")
	cursor = liwc_db.cursor()
	t = StringTrie();
	
	cursor.execute("SELECT * FROM LIWC")
	liwc_data_list = cursor.fetchall()
	# generating Trie data structure
	if DEBUG:
		print("Creating Data Structure")
	for entry in liwc_data_list:
		starString = False
		if entry[0].find('*') == -1:
			starString = False
		else:
			starString = True
		withoutStar = entry[0].replace("*","")
		if DEBUG:
			print(withoutStar + " " + entry[0])
			print(entry[1])
		if t.has_node(withoutStar):
			dummy_list = t[withoutStar]
			dummy_list.append(entry[1])
			t.setdefault(withoutStar,dummy_list)
		else:
			dummy_list = list()
			if starString:
				dummy_list.append("*")
			dummy_list.append(entry[1])
			t.setdefault(withoutStar,dummy_list)
		if DEBUG:
			print("Print the value just added : ")
			print(t[withoutStar])
	liwc_db.close()
	return t;

def get_list_of_liwc_categories():
	# open database
	liwc_db = MySQLdb.connect("localhost","nlp","nlppassword","nlp")
	cursor = liwc_db.cursor()

	cursor.execute("SELECT DISTINCT type FROM LIWC")
	data = cursor.fetchall();

	liwc_categories = []

	for entry in data:
		liwc_categories.append(entry[0])

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

