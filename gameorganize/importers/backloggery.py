from gameorganize.model.game import GameEntry, Completion
from gameorganize.model.platform import Platform, find_platform
import csv 

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
        all_db_elements = []

        for entry in data:
            completion_name = entry.get("Status", "")
            if(not completion_name): 
                completion_name = "Unplayed"

            platform_name = entry.get("ConsoleName")
            platform = find_platform(platform_name)
            if(not platform):
                platform = Platform(name=platform_name)
                all_db_elements.append(platform)

            all_db_elements.append(GameEntry(
                name = entry.get("Title"),
                platform = platform,
                completion = Completion[completion_name],
                notes = entry.get("Notes", ""),
            ))

        return all_db_elements
