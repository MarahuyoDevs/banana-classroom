import pytest
from starlette.testclient import TestClient
from banana_classroom.app import app


@pytest.fixture
def client():
    yield TestClient(app, base_url="http://testserver/")


@pytest.fixture
def student_client(client: TestClient):
    yield client


@pytest.fixture
def instructor_client(client: TestClient):
    yield client


@pytest.fixture
def admin_client(client: TestClient):
    yield client
