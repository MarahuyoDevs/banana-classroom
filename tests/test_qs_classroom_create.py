from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)
from starlette import status
import os
import boto3
import time

os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ["DYNTASTIC_REGION"],
    endpoint_url=os.environ["DYNTASTIC_HOST"],
)

if "classroom" not in dynamodb.meta.client.list_tables()["TableNames"]:
    Classroom.create_table()


class TestClassroomCreation:

    client = TestClient(service)

    "Creating a classroom with valid data. Expected output: Classroom object created successfully"

    def test_create_classroom_valid_data(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "Math Class",
                "description": "Learn math concepts",
                "instructor": "Ms. Johnson",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["title"] == "Math Class"
        assert response.json()["data"]["description"] == "Learn math concepts"
        assert response.json()["data"]["instructor"] == "Ms. Johnson"

    "Creating a classroom with optional student list. Expected output: Classroom object created with an empty student list"

    def test_create_classroom_with_empty_students_list(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "English Class",
                "description": "Improve language skills",
                "instructor": "Mr. Lee",
                "students": [],
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["title"] == "English Class"
        assert response.json()["data"]["description"] == "Improve language skills"
        assert response.json()["data"]["instructor"] == "Mr. Lee"
        assert response.json()["data"]["students"] == []

    "Creating a classroom with optional quiz list. Expected output: Classroom object created with an empty quiz list"

    def test_create_classroom_with_empty_quiz_list(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "Science Class",
                "description": "Explore the wonders of science",
                "instructor": "Dr. Smith",
                "quizzes": [],
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["title"] == "Science Class"
        assert (
            response.json()["data"]["description"] == "Explore the wonders of science"
        )
        assert response.json()["data"]["instructor"] == "Dr. Smith"
        assert response.json()["data"]["quizzes"] == []

    "Creating a classroom with missing title:. Expected output: Missing data error message (Title is required)"

    def test_create_classroom_missing_title(self):
        response = self.client.post(
            "/classroom",
            json={
                "description": "test_description",
                "instructor": "test_instructor",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Title is required"

    "Creating a classroom with missing description. Expected output: Missing data error message (Description is required)"

    def test_create_classroom_missing_description(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "test_title",
                "instructor": "test_instructor",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Description is required"

    "Creating a classroom with missing instructor. Expected output: Missing data error message (Instructor is required)"

    def test_create_classroom_missing_instructor(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "test_title",
                "description": "test_description",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Instructor is required"

    "Creating a classroom with invalid instructor. Expected output: Invalid data error message (Instructor must be a string)"

    def test_create_classroom_invalid_instructor(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "Invalid Instructor Classroom",
                "description": "Classroom description",
                "instructor": 123,  # Invalid instructor value
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Instructor must be a string"

    "Creating a classroom with invalid title. Expected output: Invalid data error message (Title must be a string)"

    def test_create_classroom_invalid_title(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": 123,  # Invalid title value
                "description": "Valid description",
                "instructor": "Valid Instructor",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert (
            response.text == "Title must be a string"
        )  # Expecting specific error message

    "Creating a classroom with long title. Expected output: Invalid data error message (Title must be at most 60 characters)"

    def test_create_classroom_long_title(self):
        # Test creating a classroom with a long title
        response = self.client.post(
            "/classroom",
            json={
                "title": "A" * 69,  # Title exceeds maximum length (100 characters)
                "description": "Valid description",
                "instructor": "Valid Instructor",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert (
            "ensure this value has at most 60 characters" in response.text
        )  # Expecting specific error message

    "Creating a classroom with long description. Expected output: Invalid data error message (Description must be at most 1000 characters)"

    def test_create_classroom_long_description(self):
        # Test creating a classroom with a long description
        response = self.client.post(
            "/classroom",
            json={
                "title": "Long Description Classroom",
                "description": "A"
                * 1001,  # Description exceeds maximum length (1000 characters)
                "instructor": "Valid Instructor",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert (
            "ensure this value has at most 1000 characters" in response.text
        )  # Expecting specific error message

    "Creating a classroom with long instructor. Expected output: Invalid data error message (Instructor must be at most 30 characters)"

    def test_create_classroom_long_instructor(self):
        # Test creating a classroom with a long instructor
        response = self.client.post(
            "/classroom",
            json={
                "title": "Long Instructor Classroom",
                "description": "Valid description",
                "instructor": "A"
                * 31,  # Instructor exceeds maximum length (100 characters)
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert (
            "ensure this value has at most 30 characters" in response.text
        )  # Expecting specific error message

    def test_performance_create_multiple_classrooms(self):
        # Input: Large number of valid classroom data
        large_number_of_data = [
            {
                "title": "Classroom 1",
                "description": "Description for Classroom 1",
                "instructor": "Instructor 1",
            },
            {
                "title": "Classroom 2",
                "description": "Description for Classroom 2",
                "instructor": "Instructor 2",
            },
            # Add more data as needed...
        ]
        start_time = time.time()  # Record start time
        for data in large_number_of_data:
            response = self.client.post("/classroom", json=data)
            # Expected Output: Classrooms created within a reasonable timeframe
            assert response.status_code == 200
            assert "data" in response.json()
        end_time = time.time()  # Record end time
        execution_time = end_time - start_time
        # Assert that the execution time is within a reasonable timeframe (e.g., 10 seconds)
        assert (
            execution_time < 10
        ), f"Execution time {execution_time} seconds exceeds expected timeframe"

    """
    "Creating a classroom without proper authorization. Expected output: Restriction of classroom creation or appropriate error"
    def test_security_unauthorized_classroom_creation(self):
        # Input: Attempt to create a classroom without proper authorization
        unauthorized_data = {...}  # Data for unauthorized classroom creation
        response = self.client.post("/classroom", json=unauthorized_data)
        # Expected Output: Restriction of classroom creation or appropriate error
        assert response.status_code != 200  # Expecting classroom creation to fail


    
    "Integration with related functionalities"
    def test_integration_with_related_functionalities(self):
        # Input: Create a classroom
        response = self.client.post(
            "/classroom",
            json={
                "title": "test_classroom_integration",
                "description": "test_description_integration",
                "instructor": "test_instructor_integration",
            },
        )
        assert response.status_code == 200
        classroom_id = response.json()["data"]["id"]

        # Test adding students
        response = self.client.post(f"/classroom/{classroom_id}/students", json={"name": "Alice"})
        assert response.status_code == 200

        # Test adding quizzes
        response = self.client.post(
            "/quiz/create",
            json={
                "title": "test_quiz_integration",
                "description": "test_description_integration",
                "instructor": "test_instructor_integration",
                "class_id": classroom_id,
                "questions": [
                    {
                        "description": "test_question_integration",
                        "options": ["test_answer_integration", "test_answer_integration", "test_answer_integration"],
                        "answer": "test_answer_integration",
                    }
                ],
                "expiration_time": "2024-03-01T00:00:00",
            },
        )
        assert response.status_code == 200
        quiz_id = response.json()["data"]["id"] 
        classroom_id = response.json()["data"]["id"]

        # Test adding students
        response = self.client.post(f"/classroom/{classroom_id}/students", json={"name": "Alice"})
        assert response.status_code == 200

        # Test adding quizzes
        response = self.client.post(
            "/quiz/create",
            json={
                "title": "test_quiz_integration",
                "description": "test_description_integration",
                "instructor": "test_instructor_integration",
                "class_id": classroom_id,
                "questions": [
                    {
                        "description": "test_question_integration",
                        "options": ["test_answer_integration", "test_answer_integration", "test_answer_integration"],
                        "answer": "test_answer_integration",
                    }
                ],
                "expiration_time": "2024-03-01T00:00:00",
            },
        )
        assert response.status_code == 200
        quiz_id = response.json()["data"]["id"]
    """
