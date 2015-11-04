import re
import os

count = 0
corpus = ""
for f in os.listdir("./"):
	if f.endswith(".txt") and f != "corpus.txt":
		inputFile = open(f)
		lines = inputFile.read()
		sections = re.split("-+\n", lines)
		for i,section in enumerate(sections):
			try:
				subsections = section.split("\n")
				if subsections[0].strip() == "Answer Description":
					answer = "\n".join(text for text in subsections[1:])
					answer = answer.strip()
					count += 1
					print count
					print answer
					print
					if count == 1:
						corpus = answer
					else:
						corpus = corpus + "\n&&&&&&&&&&&&\n" + answer
					break
			except Exception:
				print "some error occured in section",i
		inputFile.close()

outputfile = open("corpus.txt","w")
outputfile.write(corpus)
