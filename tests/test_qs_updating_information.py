import pytest
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import ( Student
)
from starlette import status

@pytest.fixture(scope="module")
def classroom_data():
    return {
        "title": "Physics Class",
        "description": "Learn physics concepts",
        "instructor": "Mr. Smith",
    }

@pytest.fixture(scope="module")
def student_data():
    return {
        "id": "123",
        "name": "John Doe",
        "completed_quizzes": [],
        "incompleted_quizzes": []
    }

@pytest.fixture(scope="function")
def create_classroom(test_client, classroom_data):
    response = test_client.post("/classroom", json=classroom_data)
    classroom_id = response.json()["data"]["id"]
    yield classroom_id
    # Clean up after each test
    test_client.delete(f"/classroom/{classroom_id}")

@pytest.fixture(scope="function")
def create_student(test_client, student_data):
    Student(**student_data)
    yield student_data["id"]
    # Clean up after each test
    test_client.delete(f"/student/{student_data['id']}")

@pytest.fixture(scope="function")
def create_classroom_with_quiz(test_client, classroom_data):
    response = test_client.post("/classroom", json=classroom_data)
    classroom_id = response.json()["data"]["id"]

    # Assume you have some way to create a quiz result for this classroom
    quiz_result_id = create_quiz_result(classroom_id)

    yield classroom_id, quiz_result_id

    # Clean up after each test
    test_client.delete(f"/classroom/{classroom_id}")

# Assuming you have a function to create a quiz result, you can define it here
def create_quiz_result(classroom_id):
    # Logic to create a quiz result and return its ID
    pass


class TestUpdateInformation:

    def test_update_classroom_title_success(self, test_client, create_classroom):
        classroom_id = create_classroom

        new_title = "Advanced Physics Class"
        update_response = test_client.put(f"/classroom/{classroom_id}", json={"title": new_title})

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["title"] == new_title

    def test_update_classroom_title_excessive_length(self, test_client, create_classroom):
        classroom_id = create_classroom

        new_title = "This is an excessively long title that exceeds the character limit"
        update_response = test_client.put(f"/classroom/{classroom_id}", json={"title": new_title})

        assert update_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "exceeds the limit" in update_response.text

    def test_update_classroom_title_with_empty_string(self, test_client, create_classroom):
        classroom_id = create_classroom

        response = test_client.put(f"/classroom/{classroom_id}", json={"title": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Title cannot be empty"
        

    def test_update_classroom_description(self, test_client, create_classroom):
        classroom_id = create_classroom

        # Attempt to update description
        new_description = "Advanced math concepts"
        response = test_client.put(
            f"/classroom/{classroom_id}",
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["description"] == new_description

    def test_update_classroom_description_excessive_length(self, test_client, create_classroom):
        classroom_id = create_classroom

        # Attempt to update the description with excessive length
        response = test_client.put(
            f"/classroom/{classroom_id}",
            json={"description": "A" * 1001},  # Exceeding the character limit
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Description length exceeds the limit"

    def test_update_classroom_description_empty_string(self, test_client, create_classroom):
        classroom_id = create_classroom

        # Attempt to update the description with an empty string
        response = test_client.put(
            f"/classroom/{classroom_id}",
            json={"description": ""},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.text == "Description cannot be empty"
    def test_update_student_name_success(self, test_client, create_student):
        student_id = create_student

        new_name = "Jane Doe"
        response = test_client.put(f"/student/{student_id}", json={"name": new_name})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == new_name

    def test_update_student_name_empty_string(self, test_client, create_student):
        student_id = create_student

        response = test_client.put(f"/student/{student_id}", json={"name": ""})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"] == "Name cannot be empty"

    
    def test_update_quiz_result_score_success(self, test_client, create_classroom_with_quiz):
        classroom_id, quiz_result_id = create_classroom_with_quiz

        # Update the quiz result score
        new_score = 90
        update_response = test_client.put(
            f"/classroom/{classroom_id}/quizzes/{quiz_result_id}",
            json={"score": new_score}
        )

        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["score"] == new_score

    def test_update_quiz_result_score_invalid_value(self, test_client, create_classroom_with_quiz):
        classroom_id, quiz_result_id = create_classroom_with_quiz

        # Attempt to update the quiz result score with an invalid value
        invalid_score = -10
        update_response = test_client.put(
            f"/classroom/{classroom_id}/quizzes/{quiz_result_id}",
            json={"score": invalid_score}
        )

        assert update_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY