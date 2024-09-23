from gameorganize.app import app
from gameorganize.db import db
import pytest

@pytest.fixture()
def test_app():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tests.sqlite3"
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()