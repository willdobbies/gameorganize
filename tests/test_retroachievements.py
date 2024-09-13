from importers.retroachievements import ImporterRA
from pathlib import Path
import json
import pytest

basedir = Path(__file__).parent

@pytest.mark.skip(reason="reduce server stress")
def test_fetch(apiId, apiKey):
    importer = ImporterRA(username=apiId, api_key=apiKey)
    fdata = importer.fetch()
    print(f"Fetched data for {len(fdata)} games")
    with open("data/retroachievements.json", "w") as buf:
        json.dump(fdata, buf)

def test_parse():
    importer = ImporterRA(None, None)
    with open(basedir / "data/retroachievements.json", "r") as buf:
        data = json.loads(buf.read())
        games = importer.parse(data)
    assert True
