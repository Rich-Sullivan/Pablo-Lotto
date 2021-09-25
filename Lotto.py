import csv
from pathlib import Path
# name of file downloaded from 
filename = "data.csv"

fields = []
rows = []
results = []
nopattern = []
price = 500
p = Path(__file__).with_name(filename)
with p.open ('r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)
for row in rows:
    if int(row[4]) % price == 0:
        tickets = int(int(row[4])/price)
        goodprice = True
    else:
        tickets = 1
        goodprice = False
    #if row[2] == "incoming" and row[3] == "purchase" and "ticket" in row[5][27:].lower():
    if row[2] == "incoming" and row[3] == "purchase" and goodprice == True:
        for i in range(tickets):
            results.append(row)
    elif row[2] == "incoming" and row[3] == "purchase":
        for i in range(tickets):
            nopattern.append(row)

#write results
f = open("result.txt", "a")
for el in results:
    f.write(el[4]+'\t'+el[5][27:].replace('\n', " ")+'\n')
f = open("mismatches.csv", "a")
for el in nopattern:
    f.write(el[4]+','+el[5][27:].replace('\n', " ")+'\n')
