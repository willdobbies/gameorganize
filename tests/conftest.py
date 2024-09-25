from gameorganize import create_app
from gameorganize.config import TestingConfig
import pytest

def pytest_addoption(parser):
    parser.addoption("--apiId", action="store")
    parser.addoption("--apiKey", action="store")

@pytest.fixture
def apiId(request):
    return request.config.getoption("--apiId")

@pytest.fixture
def apiKey(request):
    return request.config.getoption("--apiKey")

@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()