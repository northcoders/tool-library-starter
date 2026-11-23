import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    # `with` runs the app's lifespan (startup and shutdown), so anything the
    # app builds at startup is ready before the first request.
    with TestClient(app) as client:
        yield client
