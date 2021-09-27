import csv
import glob
import os
from pathlib import Path

#get name of csv file in same path as script
targetfile = os.path.dirname(os.path.abspath(__file__))+"\*.csv"
filename = glob.glob(targetfile)[0]

fields = []
rows = []
results = []
nopattern = []

#read csv file
with open (filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)

for row in rows:
    #split comment to parse # of ticket and check that it is a ticket
    words = row[5][27:].replace('-', "").split(' ')
    print(row[5][27:])
    #check if comment contains keywork ticket
    if "ticket" in row[5][27:].lower():
        isticket = True
    else:
        isticket = False
    if "membership" in row[5][27:].lower():
        ismembership = True
    else:
        ismembership = False

    #check if row is a charge and that 1st word is integer to represent # of tickets
    #if it is add it to the result list    
    if row[2] == "incoming" and row[3] == "purchase" and words[0].replace("x", "").isnumeric() == True and isticket == True:
        for i in range(int(words[0].replace("x", ""))):
            results.append(row)

    #create seperate list of transactions that dont have a comment that starts with 
    #an integer then keyword ticket, but the transaction type could be ticket sale with a bad comment ie. for the # 
    elif row[2] == "incoming" and row[3] == "purchase" and ismembership == False:
        nopattern.append(row)

#write results to text file for the randomizer
f = open("result.txt", "w")
for el in results:
    f.write(el[4]+'\t'+el[5][27:].replace('\n', " ")+'\n')
#write the non matching records to new csv file for review
f = open("mismatches.csv", "w")
for el in nopattern:
    f.write(el[4]+','+el[5][27:].replace('\n', " ")+'\n')
