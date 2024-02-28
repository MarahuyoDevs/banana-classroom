import pytest
from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service as quiz_api
from banana_classroom.services.user_service.app import service as user_api


@pytest.fixture
def quiz_client() -> TestClient:
    return TestClient(quiz_api)


@pytest.fixture
def student_token(quiz_client: TestClient) -> dict:
    response = quiz_client.post(
        "/api/security/register?type=instructor",
        json={"email": "test", "password": "test", "name": "test"},
    )
    return response.json()


@pytest.fixture
def instructor_token(quiz_client: TestClient) -> dict:
    response = quiz_client.post(
        "/api/security/register?type=instructor",
        json={"email": "test", "password": "test", "name": "test"},
    )
    return response.json()


@pytest.fixture
def admin_token(quiz_client: TestClient) -> dict:
    response = quiz_client.post(
        "/api/security/register?type=instructor",
        json={"email": "test", "password": "test", "name": "test"},
    )
    return response.json()
