import xlrd
import MySQLdb

# open database
liwc_db = MySQLdb.connect("localhost","nlp","nlppassword","nlp")

cursor = liwc_db.cursor()

def add_word(word, word_type):
	if not word or not word_type:
		return
	try:
		cursor.execute("INSERT INTO LIWC VALUES (%s,%s)", (word, word_type))
		liwc_db.commit()
	except Exception, e:
		print word + " :: " + word_type

def main():
	workbook = xlrd.open_workbook('LIWC2007dictionary poster.xls')
	liwc_sheet = workbook.sheet_by_name('Official genome')
	rows = liwc_sheet.nrows
	columns = liwc_sheet.ncols
	curr_col = 0
	while curr_col < columns:
		#scan each column
		# First row in the word type
		# Add words from rest of the rows to this table with its type
		if liwc_sheet.cell_type(0, curr_col) == 1: # 1 implies text entry
			# we found the word type
			word_type = liwc_sheet.cell_value(0, curr_col)
			curr_row = 1
			while curr_row < rows:
				if liwc_sheet.cell_type(0, curr_col) == 1:
					add_word(liwc_sheet.cell_value(curr_row, curr_col), word_type)
				curr_row += 1
		curr_col += 1
		print str(curr_col) + ": " +  word_type 
	# Commit changes


if __name__ == '__main__':
	main()

liwc_db.commit()
liwc_db.close()
