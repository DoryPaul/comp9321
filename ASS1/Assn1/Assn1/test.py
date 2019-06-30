import csv

readFile = open('result_q2.csv','r')
temp = csv.reader(readFile)

i = 0
a = []
for item in temp:
    i += 1
    if item not in a:
        a.append(item)
print(i,len(a))
