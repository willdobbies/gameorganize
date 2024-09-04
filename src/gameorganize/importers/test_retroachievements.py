from retroachievements import ImporterRetroAchievements
from pathlib import Path
import json
import pytest

basedir = Path(__file__).parent

@pytest.mark.skip(reason="reduce server stress")
def test_fetch(apiId, apiKey):
    importer = ImporterRetroAchievements(username=apiId, api_key=apiKey)
    fdata = importer.fetch()
    print("Fetched data for {} games".format(len(fdata)))
    with open("test/retroachievements.json", "w") as buf:
        json.dump(fdata, buf)

def test_parse():
    importer = ImporterRetroAchievements(None, None)
    with open(basedir / "test/retroachievements.json", "r") as buf:
        data = json.loads(buf.read())
        games = importer.parse(data)
    assert True