import pytest
from fastapi.testclient import TestClient

from cicada26.main import app

# @pytest.fixture(scope="session")  # autouse?
# async def db():
#     pass


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
