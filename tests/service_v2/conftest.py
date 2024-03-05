import pytest
from banana_classroom.service_v2.app import api_service
from starlette.testclient import TestClient


@pytest.fixture
def service_v2_client() -> TestClient:
    return TestClient(api_service)
