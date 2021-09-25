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

#temporary price of tickets
price = 500

#read csv file
with open (filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)

for row in rows:
    #calculate # of ticket based of price if invalid ie. charged $700 price @ $500 700 / 500 has remainder
    if int(row[4]) % price == 0:
        tickets = int(int(row[4])/price)
        goodprice = True
    else:
        tickets = 1
        goodprice = False
    #check if row is a charge
    #when you want to start doing membership we can do this easily if the comment for charges to buisiness account are something like
    #{# of items charged for}, {item}, {client name}, {state id}
    #ie 3, tickets, Scruffy doodle, 6876 or 1, membership, Scruffy doodle, 6876
    # this would allow for easy identification of sales type
    if row[2] == "incoming" and row[3] == "purchase" and goodprice == True:
        for i in range(tickets):
            results.append(row)

    #create seperate list of transactions that dont mathamatically make sense $ charge wise, 
    #when memberships start this would include transactions that the comments that 
    #dont include a # < 10 for # of tickets and an item type ie. ticket, or membership
    elif row[2] == "incoming" and row[3] == "purchase":
        for i in range(tickets):
            nopattern.append(row)

#write results to text file for the randomizer
f = open("result.txt", "a")
for el in results:
    f.write(el[4]+'\t'+el[5][27:].replace('\n', " ")+'\n')
#write the non matching records to new csv file for review
f = open("mismatches.csv", "a")
for el in nopattern:
    f.write(el[4]+','+el[5][27:].replace('\n', " ")+'\n')
