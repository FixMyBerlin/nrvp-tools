import csv
import json

csvfile = open(
    "Nutzergruppeneinordnung nach ModalSplit KatasterKi Nov19 - Vincents Minimalversion.csv",
    "r",
)
jsonfile = open("userGroups.json", "w")

reader = csv.DictReader(csvfile)
jsonfile.write("[\n")
for row in reader:
    json.dump(row, jsonfile, indent=2)
    jsonfile.write(",\n")
jsonfile.write("]\n")
