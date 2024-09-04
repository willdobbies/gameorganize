import csv 
import time

from gameorganize.model.game import *

# Library columns:
#    "Unique Game ID", "Title", "Platform", "Sub-Platform",
#    "Status", "Priority", "Format", "Ownership", "Notes",
#    "Child Of", "Last Updated"

class ImporterBackloggery():
    def __init__(self):
        pass

    def csv_to_json(self, path):
        jsonArray = []
        
        #read csv file
        with open(path, encoding='utf-8') as csvf: 
            #load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csvf) 

            #convert each csv row into python dict
            for row in csvReader: 
                #add this python dict to json array
                jsonArray.append(row)
    
        return jsonArray

    def parse(self, data):
        new_games = []

        for entry in data:
            completion_name = entry.get("Status", "")
            if(not completion_name): completion_name = "Unplayed"

            new_games.append(GameEntry(
                name = entry.get("Title"),
                platform = entry.get("Platform"),
                completion = Completion[completion_name],
                notes = entry.get("Notes", ""),
            ))

        return new_games
    
if (__name__ == "__main__"):
    importer = ImporterBackloggery()
    data = importer.csv_to_json("test/backloggery-library.csv")
    games = importer.parse(data)
    print(games)