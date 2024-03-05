<<<<<<< HEAD
from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
    Student,
=======
import pytest
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import ( Student
>>>>>>> origin/master
)
from starlette import status

# Fixture to create a classroom
@pytest.fixture(scope="module")
def classroom_data():
    return {
        "title": "Physics Class",
        "description": "Learn physics concepts",
        "instructor": "Mr. Smith",
    }

# Fixture to create a student
@pytest.fixture(scope="module")
def student_data():
    return {
        "id": "123",
        "name": "John Doe",
        "completed_quizzes": [],
        "incompleted_quizzes": []
    }

# Fixture to create a classroom
@pytest.fixture(scope="function")
def create_classroom(test_client, classroom_data):
    response = test_client.post("/classroom", json=classroom_data)
    classroom_id = response.json()["data"]["id"]
    yield classroom_id
    # Clean up after each test
    test_client.delete(f"/classroom/{classroom_id}")

<<<<<<< HEAD

=======
# Fixture to create a student
@pytest.fixture(scope="function")
def create_student(test_client, student_data):
    Student(**student_data)
    yield student_data["id"]
    # Clean up after each test
    test_client.delete(f"/student/{student_data['id']}")
    
@pytest.fixture(scope="function")
def create_classroom_with_quiz(test_client, classroom_data, create_quiz_result):
    response = test_client.post("/classroom", json=classroom_data)
    classroom_id = response.json()["data"]["id"]
    quiz_result_id = create_quiz_result(classroom_id) # Create a quiz result for this classroom

    def cleanup():
        test_client.delete(f"/quiz/{quiz_result_id}") # Clean up quiz result
        test_client.delete(f"/classroom/{classroom_id}") # Clean up classroom
    
    yield classroom_id, quiz_result_id # Yield the tuple of classroom ID and quiz result ID
    cleanup() # Clean up after each test

# Test class for updating classroom information
>>>>>>> origin/master
class TestUpdateInformation:

    # Test updating classroom title
    def test_update_classroom_title_success(self, test_client, create_classroom):
        classroom_id = create_classroom

<<<<<<< HEAD
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
        update_response = self.client.put(
            f"/classroom/{classroom_id}", json={"title": new_title}
        )
=======
        new_title = "Advanced Physics Class"
        update_response = test_client.put(f"/classroom/{classroom_id}", json={"title": new_title})
>>>>>>> origin/master

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["title"] == new_title

<<<<<<< HEAD
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
=======
    # Test updating classroom title
    def test_update_classroom_title_excessive_length(self, test_client, create_classroom):
        classroom_id = create_classroom
>>>>>>> origin/master

        new_title = "This is an excessively long title that exceeds the character limit"
<<<<<<< HEAD
        update_response = self.client.put(
            f"/classroom/{classroom_id}", json={"title": new_title}
        )
=======
        update_response = test_client.put(f"/classroom/{classroom_id}", json={"title": new_title})
>>>>>>> origin/master

        assert update_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "exceeds the limit" in update_response.text

<<<<<<< HEAD
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
=======
    # Test updating classroom title
    def test_update_classroom_title_with_empty_string(self, test_client, create_classroom):
        classroom_id = create_classroom
>>>>>>> origin/master

        response = test_client.put(f"/classroom/{classroom_id}", json={"title": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Title cannot be empty"
<<<<<<< HEAD

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
=======
        
    # Test class for updating classroom description
    def test_update_classroom_description(self, test_client, create_classroom):
        classroom_id = create_classroom
>>>>>>> origin/master

        # Attempt to update description
        new_description = "Advanced math concepts"
        response = test_client.put(
            f"/classroom/{classroom_id}",
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["description"] == new_description

<<<<<<< HEAD
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
=======
    # Test class for updating classroom description
    def test_update_classroom_description_excessive_length(self, test_client, create_classroom):
        classroom_id = create_classroom
>>>>>>> origin/master

        # Attempt to update the description with excessive length
        response = test_client.put(
            f"/classroom/{classroom_id}",
            json={"description": "A" * 1001},  # Exceeding the character limit
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Description length exceeds the limit"

<<<<<<< HEAD
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
=======
    # Test class for updating classroom description
    def test_update_classroom_description_empty_string(self, test_client, create_classroom):
        classroom_id = create_classroom

        # Attempt to update the description with an empty string
        response = test_client.put(
>>>>>>> origin/master
            f"/classroom/{classroom_id}",
            json={"description": ""},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Description cannot be empty"

<<<<<<< HEAD
    def test_update_student_name_success(self):
        # Creating a student record
        student_data = {
            "id": "123",
            "name": "John Doe",
            "completed_quizzes": [],
            "incompleted_quizzes": [],
        }
        Student(**student_data)
=======
    # Test class for updating student name
    def test_update_student_name_success(self, test_client, create_student):
        student_id = create_student
>>>>>>> origin/master

        new_name = "Jane Doe"
<<<<<<< HEAD
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
            "incompleted_quizzes": [],
        }
        Student(**student_data)
=======
        response = test_client.put(f"/student/{student_id}", json={"name": new_name})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == new_name

    # Test class for updating student name
    def test_update_student_name_empty_string(self, test_client, create_student):
        student_id = create_student
>>>>>>> origin/master

        response = test_client.put(f"/student/{student_id}", json={"name": ""})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"] == "Name cannot be empty"

    # Test updating quiz result score with a valid value
    def test_update_quiz_result_score_success(self, test_client, create_classroom_with_quiz):
        classroom_id, quiz_result_id = create_classroom_with_quiz

<<<<<<< HEAD
        quiz_result_id = classroom_response.json()["data"]["quizzes"][0]["id"]

=======
>>>>>>> origin/master
        # Update the quiz result score
        new_score = 90
        update_response = test_client.put(
            f"/classroom/{classroom_id}/quizzes/{quiz_result_id}",
            json={"score": new_score},
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["score"] == new_score

    # Test updating quiz result score with an invalid value
    def test_update_quiz_result_score_invalid_value(self, test_client, create_classroom_with_quiz):
        classroom_id, quiz_result_id = create_classroom_with_quiz

<<<<<<< HEAD
        quiz_result_id = classroom_response.json()["data"]["quizzes"][0]["id"]

=======
>>>>>>> origin/master
        # Attempt to update the quiz result score with an invalid value
        invalid_score = -10
        update_response = test_client.put(
            f"/classroom/{classroom_id}/quizzes/{quiz_result_id}",
            json={"score": invalid_score},
        )

        assert update_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
<<<<<<< HEAD
=======
        assert "invalid value" in update_response.json()["detail"].lower()  # Ensure response contains appropriate message
    
    """ OPTIONAL

@pytest.fixture(scope="function")
def create_classroom_with_quiz(test_client, classroom_data, create_quiz_result):
    response = test_client.post("/classroom", json=classroom_data)
    classroom_id = response.json()["data"]["id"]
    quiz_result_id = create_quiz_result(classroom_id) # Create a quiz result for this classroom

    def cleanup():
        test_client.delete(f"/quiz/{quiz_result_id}") # Clean up quiz result
        test_client.delete(f"/classroom/{classroom_id}") # Clean up classroom
    
    yield classroom_id, quiz_result_id # Yield the tuple of classroom ID and quiz result ID
    cleanup() # Clean up after each test

    def test_update_quiz_result_score_success(test_client, create_classroom_with_quiz):
        classroom_id, quiz_result_id = create_classroom_with_quiz

        # Update the quiz result score
        new_score = 90
        update_response = test_client.put(
            f"/classroom/{classroom_id}/quizzes/{quiz_result_id}",
            json={"score": new_score}
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["score"] == new_score  # Corrected to access the score directly

    def test_update_quiz_result_score_invalid_value(test_client, create_classroom_with_quiz):
        classroom_id, quiz_result_id = create_classroom_with_quiz

        # Attempt to update the quiz result score with an invalid value
        invalid_score = -10
        update_response = test_client.put(
            f"/classroom/{classroom_id}/quizzes/{quiz_result_id}",
            json={"score": invalid_score}
        )

        assert update_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # Ensure it returns 422
    """
>>>>>>> origin/master
