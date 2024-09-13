from model.game import GameEntry, Completion, Ownership
import requests

class ImporterSteam():
    def __init__(self, steamId:str, apiKey:str):
        self.steamId = steamId
        self.apiKey = apiKey

    def fetch_games(self):
        """
        Fetch info for all games belonging to a given steam user
        """
        print(f"Fetching games for steam user id {self.steamId}")
        params={
            "key":self.apiKey,
            "steamid":self.steamId,
            "include_appinfo":1,
            "include_played_free_games":1,
            "format":"json",
        }

        r = requests.get(
            "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/",
            params=params
        )

        return r.json()

    def fetch_stats(self, app_id:str):
        """
        Fetch achievement data & stats for a given appid
        """
        print(f"Fetching stats for steam appid {app_id}")
        params={
            "key":self.apiKey,
            "steamid":self.steamId,
            "appid":app_id,
            "format":"json",
        }

        r = requests.get(
            "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/",
            params=params
        )

        return r.json()

    def fetch(self):
        """
        Fetch all game info, plus achievement data for given user
        """
        
        data = self.fetch_games().get("response",{}).get("games", [])

        for idx,game in enumerate(data):
            data[idx]["stats"] = self.fetch_stats(game["appid"])
        
        return data
    
    def get_completion(self, playtime:int, stats:dict):
        """
        Get game completion based on steam api stats
        """
        cheev = stats.get("playerstats", {}).get("achievements", [])
        cheev_got = list(filter(lambda a: (a["achieved"] == 1), cheev))

        completion = Completion.Unplayed
        if(playtime > 0):
            completion = Completion.Started
        if(len(cheev) > 0 and cheev_got == cheev):
            completion = Completion.Completed

        return [completion, cheev, cheev_got]
    
    def parse(self, res:dict):
        all_games = []
        for entry in res:
            completion,cheev,cheev_got = self.get_completion(
                entry.get("playtime_forever",0),
                entry.get("stats", {})
            )

            new_game = GameEntry(
                name = entry.get("name"),
                platform = "Steam",
                completion = completion,
                ownership = Ownership.Digital,
                cheev = len(cheev_got),
                cheev_total = len(cheev)
            )

            all_games.append(new_game)

        return all_games
