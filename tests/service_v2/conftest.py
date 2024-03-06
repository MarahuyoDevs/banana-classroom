import pytest
from banana_classroom.app_v2 import app
from starlette.testclient import TestClient


@pytest.fixture
def service_v2_client() -> TestClient:
    return TestClient(app)
