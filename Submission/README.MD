DISCOURSE PARSING
-----------------
Discourse Parsing Tool Used from this Site: http://www.cs.toronto.edu/~weifeng/software.html
It creates a RST Style discoure tree given a properly formatted input text.

In the folder Discourse Parsing Results, Discourse Tree holds the RST style tree of 2000 essays. In the csv file discourse_essay_data.csv, each essay's nucleus text, the relations present and the number of times that relation has occured is present.

makeDocProper.py : segments the given text into sentences and paragraphs in the format prescribed by the software.

runParser.py : uses the software's "parse" executable to parse all the essays in the file list given in the script and outputs the RST discourse tree.

findMainNucleus.py: Extracts the nucleus text and all the relations present in the text. Does the same for all the text files and outputs the result in a csv file.