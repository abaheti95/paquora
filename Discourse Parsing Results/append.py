import csv
list_1=[]
with open('essays_updated.csv', 'rb') as f:
	    reader = csv.reader(f)
	    first_row_1 = next(reader)
	    for row in reader:
			list_1.append(row)

list_2=[]
with open('discourse_essay_data.csv', 'rb') as f:
	    reader = csv.reader(f)
	    first_row_2 = next(reader)
	    for row in reader:
			list_2.append(row)


first_row_1.extend(first_row_2[1:])
print len(first_row_1)
data=[]
print len(list_1[1])+len(list_2[0][1:])

for l in list_2:
	index=int(l[0])
	l2=list_1[index-1]
	l2.extend(l[1:])
	data.append(l2)

with open('essay_new.csv', 'a') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(data)



