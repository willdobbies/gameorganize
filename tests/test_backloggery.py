from gameorganize.importers.backloggery import ImporterBackloggery
from pathlib import Path

basedir = Path(__file__).parent

def test_import(app):
    """Test backloggery CSV import"""
    importer = ImporterBackloggery()
    data = importer.csv_to_json(basedir / "data/backloggery-library.csv")
    with app.app_context():
        games = importer.parse(data)
    assert(True)
    #print(games)
