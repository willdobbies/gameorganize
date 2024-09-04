import pytest

def pytest_addoption(parser):
    parser.addoption("--steamId", action="store")
    parser.addoption("--apiKey", action="store")


@pytest.fixture
def steamId(request):
    return request.config.getoption("--steamId")

@pytest.fixture
def apiKey(request):
    return request.config.getoption("--apiKey")