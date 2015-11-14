import sys
import os

# os.system("some_command with args")
essay_file = open("essay_list.txt","r")
lines = essay_file.read().splitlines()
for line in lines:
	os.system("./parse -o -S tagged_sentences/"+line)