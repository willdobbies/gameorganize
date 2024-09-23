from gameorganize.importers.steam import ImporterSteam
from gameorganize.model.game import Completion
from pathlib import Path
import json
import pytest
from flask_setup import test_app, client, runner

basedir = Path(__file__).parent

@pytest.mark.skip(reason="reduce server stress")
def test_fetch(apiId, apiKey):
    importer = ImporterSteam(apiId, apiKey)
    
    fdata = importer.fetch()
    assert (fdata is not None)

    print(f"Fetched data for {len(fdata)} games")
    with open(basedir / "data/steam.json", "w") as buf:
        json.dump(fdata, buf)

@pytest.mark.skip(reason="reduce server stress")
def test_fetch_stats(apiId, apiKey):
    importer = ImporterSteam(apiId, apiKey)

    stats = importer.fetch_stats(215670)
    assert (stats.get("achievements", []) is not None)

    #print(stats)

def test_completion(client):
    importer = ImporterSteam(None, None)

    completion_null = importer.get_completion(0, {})
    assert completion_null[0] == Completion.Unplayed

    with open(basedir / "data/steam-cheev1.json", "r") as buf:
        stats = json.loads(buf.read())
        completion = importer.get_completion(
            1000,
            stats
        )

        assert completion[0] == Completion.Started

    with open(basedir / "data/steam-cheev3.json", "r") as buf:
        stats = json.loads(buf.read())
        completion = importer.get_completion(
            1000,
            stats
        )

        #print(stats)
        #print(completion[1])
        #print(completion[2])

        assert completion[0] == Completion.Completed

def test_parse(client):
    importer = ImporterSteam(None, None)

    with open(basedir / "data/steam.json", "r") as buf:
        data = json.loads(buf.read())
        games = importer.parse(data)
        #print(games)
    assert True
