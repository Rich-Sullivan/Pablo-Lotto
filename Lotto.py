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

    #iterate through comment to find integers
    numbers = []
    number = ""
    tickets = "0"
    for element in row[5][27:]:        
        if element.isnumeric():
            if len(number) > 0:
                number = number + element
            else:
               number = element
        else:
            if len(number) > 0:
                if int(number) <= 10 and int(number) > 0:
                    numbers.append(number)
                number = ""
    #check that comment includes keyword ticket and only has 1 valid integer
    if ("ticket" in row[5][27:].lower()) == True and len(numbers) == 1:
        isticket = True
        tickets = numbers[0]
    else:
        isticket = False    
        
    
    #check if row is a charge
    #if it is add it to the result list and had a valid # of tickets
    if row[2] == "incoming" and row[3] == "purchase" and isticket == True:
        row.append(tickets)
        for i in range(int(tickets)):
            results.append(row)

    #create seperate list of transactions that dont have a comment that starts with 
    #an integer then keyword ticket, but the transaction type could be ticket sale with a bad comment ie. for the # 
    elif row[2] == "incoming" and row[3] == "purchase" and ("membership" in row[5][27:].lower()) == False:
        nopattern.append(row)
    elif row[2] == "outgoing" and row[3] == "transfer" and ("win" in row[5].lower()) == True:
        results.clear()
        nopattern.clear()

#write results to text file for the randomizer
f = open("result.txt", "w")
for el in results:
    f.write(str(int((int(el[4])/int(el[8]))))+'\t'+el[5][27:].replace('\n', " ")+'\n')
#write the non matching records to new csv file for review
f = open("mismatches.csv", "w")
for el in nopattern:
    f.write(el[4]+','+el[5][27:].replace('\n', " ")+'\n')
