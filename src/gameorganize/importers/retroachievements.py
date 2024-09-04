import requests

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