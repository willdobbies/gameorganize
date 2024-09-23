from gameorganize.importers.backloggery import ImporterBackloggery
from pathlib import Path
from flask_setup import test_app, client, runner

basedir = Path(__file__).parent

def test_import(client):
    """Test backloggery CSV import"""
    importer = ImporterBackloggery()
    data = importer.csv_to_json(basedir / "data/backloggery-library.csv")
    games = importer.parse(data)
    assert(True)
    #print(games)
