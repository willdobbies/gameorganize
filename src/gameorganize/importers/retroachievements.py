import requests
import json

from gameorganize.model.game import GameEntry, Completion

class ImporterRetroAchievements():
    def __init__(self, username:str, api_key:str):
        self.username = username
        self.api_key = api_key

    def fetch(self):
        params = {
            "z": self.username, 
            "y": self.api_key, 
            "u": self.username 
        }

        r = requests.get(
            "https://retroachievements.org/API/API_GetUserCompletionProgress.php", 
            params=params
        )

        return r.json()

    def parse(self, res : dict):
        all_games = []

        for entry in res.get("Results", []):
            completion = Completion.Started
            completion_award = entry.get("HighestAwardKind")
            if(completion_award):
                if("beaten" in completion_award):
                    completion = Completion.Beaten
                if("mastered" in completion_award):
                    completion = Completion.Completed

            new_game = GameEntry(
                name = entry.get("Title"),
                platform = entry.get("ConsoleName"),
                completion = completion,
                cheev = entry.get("NumAwarded", 0),
                cheev_total = entry.get("MaxPossible", 0)
            )

            all_games.append(new_game)
        
        return all_games

if (__name__ == "__main__"):
    import sys

    importer = ImporterRetroAchievements(username=sys.argv[1], api_key=sys.argv[2])

    ## Test fetch
    #fdata = importer.fetch()
    #print("Fetched data for {} games".format(len(fdata)))
    #with open("test/retroachievements.json", "w") as buf:
    #    json.dump(fdata, buf)

    # Test parse
    with open("test/retroachievements.json", "r") as buf:
        data = json.loads(buf.read())
        games = importer.parse(data)
        print(games)