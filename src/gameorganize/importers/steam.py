import requests
import json
import pytest

from gameorganize.model.game import GameEntry, Completion, Ownership

class ImporterSteam():
    def __init__(self, steamId:str, apiKey:str):
        self.steamId = steamId
        self.apiKey = apiKey

    def fetch_games(self):
        """
        Fetch info for all games belonging to a given steam user
        """
        print("Fetching games for steam user id {}".format(self.steamId))
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
        print("Fetching stats for steam appid {}".format(app_id))
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
                cheev = len(cheev),
                cheev_total = len(cheev_got)
            )

            all_games.append(new_game)

        return all_games

@pytest.mark.skip(reason="reduce server stress")
def test_fetch(steamId, apiKey):
    importer = ImporterSteam(steamId, apiKey)
    
    fdata = importer.fetch()
    assert (fdata is not None)

    print("Fetched data for {} games".format(len(fdata)))
    with open("test/steam.json", "w") as buf:
        json.dump(fdata, buf)

@pytest.mark.skip(reason="reduce server stress")
def test_fetch_stats(steamId, apiKey):
    importer = ImporterSteam(steamId, apiKey)

    stats = importer.fetch_stats(215670)
    assert (stats.get("achievements", []) is not None)

    print(stats)

def test_completion(steamId, apiKey):
    importer = ImporterSteam(steamId, apiKey)

    completion_null = importer.get_completion(0, {})
    assert completion_null[0] == Completion.Unplayed

    with open("test/steam-cheev1.json", "r") as buf:
        stats = json.loads(buf.read())
        completion = importer.get_completion(
            1000,
            stats
        )

        assert completion[0] == Completion.Started

    with open("test/steam-cheev3.json", "r") as buf:
        stats = json.loads(buf.read())
        completion = importer.get_completion(
            1000,
            stats
        )

        print(stats)
        print(completion[1])
        print(completion[2])

        assert completion[0] == Completion.Completed

def test_parse(steamId, apiKey):
    importer = ImporterSteam(steamId, apiKey)

    with open("test/steam.json", "r") as buf:
        data = json.loads(buf.read())
        games = importer.parse(data)
        print(games)
    assert True