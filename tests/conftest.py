import pytest
from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import Classroom
import os
import boto3

# Fixture to set up DynamoDB environment
@pytest.fixture(scope="module")
def dynamodb():
    os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
    os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"

    dynamodb_resource = boto3.resource(
        "dynamodb",
        region_name=os.environ["DYNTASTIC_REGION"],
        endpoint_url=os.environ["DYNTASTIC_HOST"],
    )

    if "classroom" not in dynamodb_resource.meta.client.list_tables()["TableNames"]:
        Classroom.create_table()

    yield dynamodb_resource

# Fixture to create a test client
@pytest.fixture(scope="module")
def test_client():
    return TestClient(service)

# Fixture to set up a classroom for testing
@pytest.fixture(scope="function")
def setup_classroom(dynamodb):    #test_qs_classroom_student
    classroom = Classroom(title="Math Class", description="Learn math concepts", instructor="Ms. Johnson")
    classroom.save()
    yield classroom.id
    classroom.delete()
