from gameorganize import create_app
from gameorganize.config import TestingConfig
from gameorganize.db import db
import pytest

def pytest_addoption(parser):
    parser.addoption("--apiId", action="store")
    parser.addoption("--apiKey", action="store")

@pytest.fixture()
def apiId(request):
    return request.config.getoption("--apiId")

@pytest.fixture()
def apiKey(request):
    return request.config.getoption("--apiKey")

@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    yield app

@pytest.fixture()
def app_client(app):
    return app.test_client()

@pytest.fixture()
def app_runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def db_session(app):
    with app.app_context():
        try:
            #db.create_all()
            yield db.session
            db.session.rollback()
            db.session.close()
        finally:
            db.drop_all()
