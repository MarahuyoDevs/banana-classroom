import pytest
from banana_classroom.service_v2.app import api_service
from banana_classroom.frontend.app import frontend_app
from starlette.testclient import TestClient


@pytest.fixture
def service_v2_backend_client() -> TestClient:
    return TestClient(api_service)


@pytest.fixture
def service_v2_frontend_client() -> TestClient:
    return TestClient(frontend_app)
