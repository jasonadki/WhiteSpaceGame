import csv
import json

finalList = []
# Read in "abv2.csv" For each row add every element to a list
with open("abv2.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        miniList = []
        for i in range(len(row)):
            miniList.append(row[i])

        # Remove empty strings
        miniList = [i for i in miniList if i != '']
        finalList.append(miniList)

with open("syn2.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        miniList = []
        for i in range(len(row)):
            miniList.append(row[i])

        # Remove empty strings
        miniList = [i for i in miniList if i != '']
        finalList.append(miniList)
    

# Save the list to a json file
with open("replacements.json", "w") as f:
    json.dump(finalList, f)
