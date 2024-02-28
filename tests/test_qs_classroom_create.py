import unittest
from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import Classroom
import os
import boto3

os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"

dynamodb = boto3.resource(
    "dynamodb", region_name="ap-southeast-1", endpoint_url="http://localhost:8000"
)

if "classroom" not in dynamodb.meta.client.list_tables()["TableNames"]:
    Classroom.create_table()

class TestClassroomCreation(unittest.TestCase):

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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["title"], "Math Class")
        self.assertEqual(response.json()["data"]["description"], "Learn math concepts")
        self.assertEqual(response.json()["data"]["instructor"], "Ms. Johnson")

    "Creating a classroom with optional student list. Expected output: Classroom object created with an empty student list"
    def test_create_classroom_with_empty_students_list(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "English Class",
                "description": "Improve language skills",
                "instructor": "Mr. Lee",
                "students": []
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["title"], "English Class")
        self.assertEqual(response.json()["data"]["description"], "Improve language skills")
        self.assertEqual(response.json()["data"]["instructor"], "Mr. Lee")
        self.assertEqual(response.json()["data"]["students"], [])

    "Creating a classroom with optional quiz list. Expected output: Classroom object created with an empty quiz list"
    def test_create_classroom_with_empty_quiz_list(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "Science Class",
                "description": "Explore the wonders of science",
                "instructor": "Dr. Smith",
                "quizzes": []
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["title"], "Science Class")
        self.assertEqual(response.json()["data"]["description"], "Explore the wonders of science")
        self.assertEqual(response.json()["data"]["instructor"], "Dr. Smith")
        self.assertEqual(response.json()["data"]["quizzes"], [])

    "Creating a classroom with missing title:. Expected output: Missing data error message (Title is required)"
    def test_create_classroom_missing_title(self):
        response = self.client.post(
            "/classroom",
            json={
                "description": "test_description",
                "instructor": "test_instructor",
            },
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"][0]["msg"], "field required")
        self.assertEqual(response.json()["detail"][0]["type"], "value_error.missing")

    "Creating a classroom with missing description. Expected output: Missing data error message (Description is required)"
    def test_create_classroom_missing_description(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "test_title",
                "instructor": "test_instructor",
            },
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"][0]["msg"], "field required")
        self.assertEqual(response.json()["detail"][0]["type"], "value_error.missing")

    "Creating a classroom with missing instructor. Expected output: Missing data error message (Instructor is required)"
    def test_create_classroom_missing_instructor(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "test_title",
                "description": "test_description",
            },
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"][0]["msg"], "field required")
        self.assertEqual(response.json()["detail"][0]["type"], "value_error.missing")

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
        self.assertEqual(response.status_code, 422)  # Expecting validation error
        self.assertIn("Instructor must be a string", response.text)  # Expecting specific error message

    "Creating a classroom with duplicate ID. Expected output: Bad request error message (Classroom with this ID already exists)"
    def test_create_classroom_duplicate_id(self):
        # Test creating a classroom with duplicate ID
        # First, create a valid classroom
        response_valid = self.client.post(
            "/classroom",
            json={
                "title": "Valid Classroom",
                "description": "Valid description",
                "instructor": "Valid Instructor",
            },
        )
        classroom_id = response_valid.json()["data"]["id"]

        # Now, attempt to create another classroom with the same ID
        response_duplicate = self.client.post(
            "/classroom",
            json={
                "id": classroom_id,  # Duplicate ID
                "title": "Duplicate ID Classroom",
                "description": "Another classroom",
                "instructor": "Another Instructor",
            },
        )
        self.assertEqual(response_duplicate.status_code, 400)  # Expecting bad request due to duplicate ID
        self.assertIn("Classroom with this ID already exists", response_duplicate.text)  # Expecting specific error message

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
        self.assertEqual(response.status_code, 422)  # Expecting validation error
        self.assertIn("Title must be a string", response.text)  # Expecting specific error message

    "Creating a classroom with long title. Expected output: Invalid data error message (Title must be at most 100 characters)"
    def test_create_classroom_long_title(self):
        # Test creating a classroom with a long title
        response = self.client.post(
            "/classroom",
            json={
                "title": "A" * 101,  # Title exceeds maximum length (100 characters)
                "description": "Valid description",
                "instructor": "Valid Instructor",
            },
        )
        self.assertEqual(response.status_code, 422)  # Expecting validation error
        self.assertIn("ensure this value has at most 100 characters", response.text)  # Expecting specific error message

    "Creating a classroom with long description. Expected output: Invalid data error message (Description must be at most 1000 characters)"
    def test_create_classroom_long_description(self):
        # Test creating a classroom with a long description
        response = self.client.post(
            "/classroom",
            json={
                "title": "Long Description Classroom",
                "description": "A" * 1001,  # Description exceeds maximum length (1000 characters)
                "instructor": "Valid Instructor",
            },
        )
        self.assertEqual(response.status_code, 422)  # Expecting validation error
        self.assertIn("ensure this value has at most 1000 characters", response.text)  # Expecting specific error message

    "Creating a classroom with long instructor. Expected output: Invalid data error message (Instructor must be at most 100 characters)"
    def test_create_classroom_long_instructor(self):
        # Test creating a classroom with a long instructor
        response = self.client.post(
            "/classroom",
            json={
                "title": "Long Instructor Classroom",
                "description": "Valid description",
                "instructor": "A" * 101,  # Instructor exceeds maximum length (100 characters)
            },
        )
        self.assertEqual(response.status_code, 422)  # Expecting validation error
        self.assertIn("ensure this value has at most 100 characters", response.text)  # Expecting specific error message

    "Creating multiple classrooms. Expected output: Classrooms created within a reasonable timeframe"
    def test_performance_create_multiple_classrooms(self):
        # Input: Large number of valid classroom data
        large_number_of_data = [...]  # List containing a large number of valid classroom data
        for data in large_number_of_data:
            response = self.client.post("/classroom", json=data)
            # Expected Output: Classrooms created within a reasonable timeframe
            self.assertEqual(response.status_code, 200)
            self.assertIn("data", response.json())
            # Additional assertions as needed for response data

    "Creating a classroom without proper authorization. Expected output: Restriction of classroom creation or appropriate error"
    def test_security_unauthorized_classroom_creation(self):
        # Input: Attempt to create a classroom without proper authorization
        unauthorized_data = {...}  # Data for unauthorized classroom creation
        response = self.client.post("/classroom", json=unauthorized_data)
        # Expected Output: Restriction of classroom creation or appropriate error
        self.assertNotEqual(response.status_code, 200)  # Assuming unauthorized requests return a non-200 status code
        # Additional assertions as needed for response data

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
        self.assertEqual(response.status_code, 200)
        classroom_id = response.json()["data"]["id"]

        # Test adding students
        # Example: Add a student to the classroom
        response = self.client.post(f"/classroom/{classroom_id}/students", json={"name": "Alice"})
        self.assertEqual(response.status_code, 200)
        # Additional assertions as needed for response data

        # Test adding quizzes
        # Example: Create a quiz for the classroom
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
        self.assertEqual(response.status_code, 200)
        quiz_id = response.json()["data"]["id"]

if __name__ == '__main__':
    unittest.main()
