from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom, Student
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

class TestUpdateInformation:

    client = TestClient(service)

    "Updating classroom title successfully"
    def test_update_classroom_title_success(self):
        # Create a classroom to update its title
        response = self.client.post(
            "/classroom",
            json={
                "title": "Physics Class",
                "description": "Learn physics concepts",
                "instructor": "Mr. Smith",
            },
        )
        classroom_id = response.json()["data"]["id"]

        # Update classroom title
        new_title = "Advanced Physics Class"
        update_response = self.client.put(f"/classroom/{classroom_id}", json={"title": new_title})

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["title"] == new_title

    "Updating classroom title with excessive length"
    def test_update_classroom_title_excessive_length(self):
        # Create a classroom to update its title
        response = self.client.post(
            "/classroom",
            json={
                "title": "Biology Class",
                "description": "Study of living organisms",
                "instructor": "Dr. Johnson",
            },
        )
        classroom_id = response.json()["data"]["id"]

        # Attempt to update classroom title with excessive length
        new_title = "This is an excessively long title that exceeds the character limit"
        update_response = self.client.put(f"/classroom/{classroom_id}", json={"title": new_title})

        assert update_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "exceeds the limit" in update_response.text

    "Update classroom title with an empty string. Expected output: Title cannot be empty"
    def test_update_classroom_title_with_empty_string(self):
        # Create a classroom to update
        response = self.client.post(
            "/classroom",
            json={
                "title": "Math Class",
                "description": "Learn math concepts",
                "instructor": "Ms. Johnson",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        classroom_id = response.json()["data"]["id"]

        # Attempt to update title with an empty string
        response = self.client.put(
            f"/classroom/{classroom_id}",
            json={"title": ""},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Title cannot be empty"

    "Successfully update classroom description. Expected output: Classroom description is updated successfully in the system."
    def test_update_classroom_description(self):
        # Create a classroom to update
        response = self.client.post(
            "/classroom",
            json={
                "title": "Math Class",
                "description": "Learn math concepts",
                "instructor": "Ms. Johnson",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        classroom_id = response.json()["data"]["id"]

        # Attempt to update description
        new_description = "Advanced math concepts"
        response = self.client.put(
            f"/classroom/{classroom_id}",
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["description"] == new_description

    "Updating a classroom description with excessive length. Expected output: System throws an error message indicating description length exceeds the limit."
    def test_update_classroom_description_excessive_length(self):
        # Create a classroom with initial description
        initial_response = self.client.post(
            "/classroom",
            json={
                "title": "Physics Class",
                "description": "Basic physics concepts",
                "instructor": "Dr. Johnson",
            },
        )
        classroom_id = initial_response.json()["data"]["id"]
        
        # Attempt to update the description with excessive length
        response = self.client.put(
            f"/classroom/{classroom_id}",
            json={"description": "A" * 1001},  # Exceeding the character limit
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Description length exceeds the limit"

    "Updating a classroom description with empty string. Expected output: System throws an error message indicating description cannot be empty."
    def test_update_classroom_description_empty_string(self):
        # Create a classroom with initial description
        initial_response = self.client.post(
            "/classroom",
            json={
                "title": "Chemistry Class",
                "description": "Basic chemistry principles",
                "instructor": "Dr. Smith",
            },
        )
        classroom_id = initial_response.json()["data"]["id"]
        
        # Attempt to update the description with empty string
        response = self.client.put(
            f"/classroom/{classroom_id}",
            json={"description": ""},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Description cannot be empty"

    def test_update_student_name_success(self):
        # Creating a student record
        student_data = {
            "id": "123",
            "name": "John Doe",
            "completed_quizzes": [],
            "incompleted_quizzes": []
        }
        Student(**student_data)

        # Updating student name
        new_name = "Jane Doe"
        response = self.client.put("/student/123", json={"name": new_name})
        
        # Checking if update is successful
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == new_name

    def test_update_student_name_empty_string(self):
        # Creating a student record
        student_data = {
            "id": "456",
            "name": "John Doe",
            "completed_quizzes": [],
            "incompleted_quizzes": []
        }
        Student(**student_data)

        # Attempting to update student name with empty string
        response = self.client.put("/student/456", json={"name": ""})

        # Checking if an error message is thrown
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"] == "Name cannot be empty"

    def test_update_quiz_result_score_success(self):
        # Create a classroom with a quiz result
        classroom_data = {
            "title": "Math Class",
            "description": "Learn math concepts",
            "instructor": "Ms. Johnson",
            "quizzes": [
                {
                    "title": "Math Quiz",
                    "description": "Test your math skills",
                    "instructor": "Ms. Johnson",
                    "questions": [
                        {"description": "What is 2 + 2?", "answer": "4"},
                        {"description": "What is 5 * 5?", "answer": "25"},
                    ],
                }
            ],
        }
        classroom_response = self.client.post("/classroom", json=classroom_data)
        classroom_id = classroom_response.json()["data"]["id"]

        quiz_result_id = classroom_response.json()["data"]["quizzes"][0]["id"]
        
        # Update the quiz result score
        new_score = 90
        update_response = self.client.put(
            f"/classroom/{classroom_id}/quizzes/{quiz_result_id}",
            json={"score": new_score}
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["score"] == new_score

    def test_update_quiz_result_score_invalid_value(self):
        # Create a classroom with a quiz result
        classroom_data = {
            "title": "Math Class",
            "description": "Learn math concepts",
            "instructor": "Ms. Johnson",
            "quizzes": [
                {
                    "title": "Math Quiz",
                    "description": "Test your math skills",
                    "instructor": "Ms. Johnson",
                    "questions": [
                        {"description": "What is 2 + 2?", "answer": "4"},
                        {"description": "What is 5 * 5?", "answer": "25"},
                    ],
                }
            ],
        }
        classroom_response = self.client.post("/classroom", json=classroom_data)
        classroom_id = classroom_response.json()["data"]["id"]

        quiz_result_id = classroom_response.json()["data"]["quizzes"][0]["id"]
        
        # Attempt to update the quiz result score with an invalid value
        invalid_score = -10
        update_response = self.client.put(
            f"/classroom/{classroom_id}/quizzes/{quiz_result_id}",
            json={"score": invalid_score}
        )

        assert update_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY