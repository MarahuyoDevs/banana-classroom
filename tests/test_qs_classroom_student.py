import pytest
from starlette import status

@pytest.fixture
def student_data():
    return {
        "id": "test_student_id",
        "name": "Test Student",
        "completed_quizzes": ["quiz1", "quiz2"],
        "incompleted_quizzes": [],
    }

# Test class for classroom student management
class TestClassroomStudentManagement:

    # Adding a student to an existing class
    def test_add_student_to_class(self, test_client, setup_classroom):
        classroom_id = setup_classroom
        response = test_client.post(
            f"/classroom/{classroom_id}/add_student",
            json={"student_id": "123456", "student_name": "John Doe"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "John Doe" in response.json()["data"]["students"]

    # Removing a student from an existing class
    def test_remove_student_from_class(self, test_client, setup_classroom):
        classroom_id = setup_classroom
        response = test_client.post(
            f"/classroom/{classroom_id}/remove_student",
            json={"student_id": "123456"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "123456" not in response.json()["data"]["students"]

    # Adding a student who is already enrolled in the class
    def test_add_student_already_in_class(self, test_client, setup_classroom):
        classroom_id = setup_classroom
        response = test_client.put(
            f"/classroom/{classroom_id}/add_student", json={"student_id": "123456"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"message": "Student is already part of the class roster"}

    # Removing a student who is not enrolled in the class
    def test_remove_nonexistent_student(self, test_client, setup_classroom):
        classroom_id = setup_classroom
        response = test_client.put(
            f"/classroom/{classroom_id}/remove_student",
            json={"student_id": "nonexistent_student_id"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"message": "Student not found in the class roster"}

    # Adding a student with completed and incompleted quizzes
    def test_add_student_with_completed_quizzes(self, test_client, setup_classroom, student_data):
        classroom_id = setup_classroom
        response = test_client.post(f"/classroom/{classroom_id}/student", json=student_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["id"] == student_data["id"]
        assert response.json()["data"]["completed_quizzes"] == student_data["completed_quizzes"]
        assert response.json()["data"]["incompleted_quizzes"] == student_data["incompleted_quizzes"]

    # Removing a student with completed and incompleted quizzes
    def test_remove_student_with_completed_quizzes(self, test_client, setup_classroom, student_data):
        classroom_id = setup_classroom
        # Add student with completed quizzes
        test_client.post(f"/classroom/{classroom_id}/student", json=student_data)
        # Remove student
        response = test_client.delete(f"/classroom/{classroom_id}/student/{student_data['id']}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["id"] == student_data["id"]
        assert response.json()["data"]["completed_quizzes"] == student_data["completed_quizzes"]
        assert response.json()["data"]["incompleted_quizzes"] == student_data["incompleted_quizzes"]
