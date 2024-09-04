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