from starlette.testclient import TestClient
from banana_classroom.app import app
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)
from starlette import status
import os
import boto3

os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ["DYNTASTIC_REGION"],
    endpoint_url=os.environ["DYNTASTIC_HOST"],
)

if "classroom" not in dynamodb.meta.client.list_tables()["TableNames"]:
    Classroom.create_table()


class TestQuizCreation:

    "Creating a quiz with valid data. Expected output: Quiz object created successfully"

    def test_create_quiz_valid_data(self, client: TestClient):
        response = client.post(
            "/quiz/",
            json={
                "title": "Test Quiz",
                "description": "This is a test quiz",
                "instructor": "John Doe",
                "questions": [],
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["title"] == "Test Quiz"
        assert response.json()["data"]["description"] == "This is a test quiz"
        assert response.json()["data"]["instructor"] == "John Doe"
        assert response.json()["data"]["questions"] == []

    "Creating a quiz with optional student list. Expected output: Quiz object created with an empty student list"

    def test_create_quiz_with_empty_students_list(self, client: TestClient):
        response = client.post(
            "/quiz",
            json={
                "title": "Test Quiz",
                "description": "This is a test quiz",
                "instructor": "John Doe",
                "students": [],
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["title"] == "Test Quiz"
        assert response.json()["data"]["description"] == "This is a test quiz"
        assert response.json()["data"]["instructor"] == "John Doe"
        assert response.json()["data"]["students"] == []

    "Creating a quiz with missing mandatory fields. Expected output: Validation error"

    def test_create_quiz_missing_mandatory_fields(self, client: TestClient):
        response = client.post(
            "/quiz",
            json={"title": "Test Quiz"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "description" in response.json()["detail"]

    "Creating a classroom with duplicate title. Expected output: Validation error"

    def test_create_classroom_with_duplicate_title(self, client: TestClient):
        response = client.post(
            "/classroom",
            json={
                "title": "Math Class",
                "description": "Learn math concepts",
                "instructor": "Ms. Johnson",
            },
        )
        assert response.status_code == status.HTTP_200_OK

        # Attempt to create another classroom with the same title
        response_duplicate = client.post(
            "/classroom",
            json={
                "title": "Math Class",
                "description": "Another math class",
                "instructor": "Mr. Smith",
            },
        )
        assert response_duplicate.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response_duplicate.json()["message"]
            == "A classroom with the title 'Math Class' already exists. Consider using a different title."
        )

    "Creating a quiz with questions. Expected output: Quiz object created with questions"

    def test_add_questions_to_quiz(self, client: TestClient):
        response_create_quiz = client.post(
            "/quiz",
            json={
                "title": "Math Quiz",
                "description": "Test your math skills",
                "instructor": "Mr. Brown",
                "questions": [
                    {
                        "description": "What is the capital of France?",
                        "options": ["Paris", "London", "Berlin"],
                        "answer": "Paris",
                    },
                    {
                        "description": "2 + 2 = ?",
                        "options": ["1", "2", "4"],
                        "answer": "4",
                    },
                ],
            },
        )
        assert response_create_quiz.status_code == status.HTTP_200_OK
        assert response_create_quiz.json()["data"]["title"] == "Math Quiz"
        assert len(response_create_quiz.json()["data"]["questions"]) == 2

    "Creating a quiz with students. Expected output: Quiz object created with students"

    def test_create_quiz_assign_students(self, client: TestClient):
        quiz_data = {
            "title": "Class Quiz",
            "description": "Test quiz",
            "instructor": "Mr. Smith",
            "students": ["student1", "student2"],
        }

        response = client.post("/create-quiz", json=quiz_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["title"] == "Class Quiz"
        assert response.json()["data"]["students"] == ["student1", "student2"]

    "Creating a quiz with duplicate questions. Expected output: Validation error"

    def test_create_quiz_with_duplicate_questions(self, client: TestClient):
        quiz_data = {
            "title": "Duplicate Questions Quiz",
            "description": "Quiz with duplicate questions",
            "instructor": "Ms. Davis",
            "questions": [
                {
                    "description": "What is 1 + 1?",
                    "options": ["1", "2", "3"],
                    "answer": "2",
                },
                {
                    "description": "What is 2 + 2?",
                    "options": ["2", "3", "4"],
                    "answer": "4",
                },
                {
                    "description": "What is 1 + 1?",
                    "options": ["1", "2", "3"],
                    "answer": "2",
                },
            ],
        }

        response = client.post("/create-quiz", json=quiz_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Questions must be unique" in response.json()["detail"]
