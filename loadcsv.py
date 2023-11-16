import csv

f = open("demofile2.txt", "a")
with open('WGUPS Distance Table.csv', newline='') as csvFile:
    rd = csv.reader(csvFile, delimiter=',')
    

f.close()