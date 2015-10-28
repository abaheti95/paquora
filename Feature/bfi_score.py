import csv
from collections import defaultdict
def getscore_decreasing(input):
	if input=='Strongly Disagree':
		score=5
	elif input=='Disagree':
		score=4
	elif input=='Neutral':
		score=3
	elif input=='Agree':
		score=2
	elif input=='Strongly Agree':
		score=1
	return score

def getscore_increasing(input):
	if input=='Strongly Disagree':
		score=1
	elif input=='Disagree':
		score=2
	elif input=='Neutral':
		score=3
	elif input=='Agree':
		score=4
	elif input=='Strongly Agree':
		score=5
	return score	

person=[]
d = defaultdict(list)
with open('bfi.csv', 'rb') as f:
    reader = csv.reader(f)
    for idx,row in enumerate(reader):
    	l=[]
    	O_count,C_count,E_count,A_count,N_count=0,0,0,0,0
        O_count=getscore_decreasing(row[7])+getscore_increasing(row[12])
        C_count=getscore_decreasing(row[5])+getscore_increasing(row[10])
        E_count=getscore_decreasing(row[3])+getscore_increasing(row[8])
        A_count=getscore_decreasing(row[4])+getscore_increasing(row[9])
        N_count=getscore_decreasing(row[6])+getscore_increasing(row[11])
        
        d[row[0]].extend((row[1],O_count,C_count,E_count,A_count,N_count))
       
        
#print d['Ayush bajpai'][3]
