import pytest
import os
import boto3
from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import Classroom

# Set up environment variables
os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"

@pytest.fixture(scope="module")
def dynamodb():
    # Set up DynamoDB resource
    dynamodb = boto3.resource(
        "dynamodb", region_name="ap-southeast-1", endpoint_url="http://localhost:8000"
    )

    # Create Classroom table if not exists
    if "classroom" not in dynamodb.meta.client.list_tables()["TableNames"]:
        Classroom.create_table()

    yield dynamodb

@pytest.fixture(scope="module")
def test_client():
    # Set up test client
    client = TestClient(service)
    yield client

@pytest.fixture(scope="module")
def valid_classroom_id():
    return "classroom"

@pytest.fixture(scope="module")
def valid_student_id():
    return "student"

@pytest.fixture(scope="module")
def invalid_classroom_id():
    return "invalid"

@pytest.fixture(scope="module")
def invalid_student_id():
    return "invalid"

@pytest.fixture(scope="module")
def classroom_data():
    # Provide test data for Classroom
    return {}  # Add test data as needed

@pytest.fixture(scope="module")
def quiz_data():
    # Provide test data for Quiz
    return {}  # Add test data as needed
