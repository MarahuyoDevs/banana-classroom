import pytest
import os

# Set up environment variables
os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"

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

class TestJoinClassroom:

    def test_join_valid_link(self, test_client, valid_classroom_id, valid_student_id):
        # Attempt to join a classroom with the given link
        response = test_client.get(
            f"/classroom/join?class-id={valid_classroom_id}&student-id={valid_student_id}"
        )
        assert response.status_code == 200
        assert "success" == response.json()["status"]
        assert valid_student_id == response.json()["data"]["students"]

    def test_join_invalid_link(self, test_client, invalid_classroom_id, valid_student_id):
        # Attempt to join a classroom with an invalid link
        response = test_client.get(
            f"/classroom/join?class-id={invalid_classroom_id}&student-id={valid_student_id}"
        )
        assert response.status_code == 404
        assert "error" == response.json()["status"]
        assert "Invalid link" == response.json()["message"]

    def test_submit_quiz(self, test_client, classroom_data, quiz_data):
        # Get a list of completed quizzes
        response = test_client.post(
            "/quiz/submit",
            json={
                "class_id": classroom_data["id"],
                "quiz_id": quiz_data["id"],
                "description": "test_quiz",
                "instructor": "test_instructor",
                "answers": [
                    {
                        "question_id": quiz_data["questions"][0]["id"],
                        "answer": quiz_data["questions"][0]["answer"],
                    },
                ],
            },
        )
        assert response.status_code == 200
        assert response.json()["score"] == len(
            [x for x in response.json()["questions"] if x]
        )

    def test_get_incomplete_quizzes(self, test_client):
        # Get a list of incomplete quizzes
        response = test_client.get("/student/incomplete_quizzes")
        # Check expected output
        expected_output = [
            {"id": "quiz_id_1", "title": "Incomplete Quiz 1"},
            {"id": "quiz_id_2", "title": "Incomplete Quiz 2"},
        ]
        assert response.status_code == 200
        assert response.json() == expected_output

    def test_student_finished_quiz(self, quiz_data):
        # Student finished a quiz
        student_id = "student123"
        # Mocking the completion of a quiz by adding its ID to completed_quizzes
        student = {"id": student_id, "completed_quizzes": [], "incompleted_quizzes": []}
        student["completed_quizzes"].append(quiz_data["id"])
        assert quiz_data["id"] == student["completed_quizzes"]

    def test_student_failed_quiz(self, quiz_data):
        # Student failed a quiz
        student_id = "student456"
        # Mocking the failure of a quiz by adding its ID to incompleted_quizzes
        student = {"id": student_id, "completed_quizzes": [], "incompleted_quizzes": []}
        student["incompleted_quizzes"].append(quiz_data["id"])
        assert quiz_data["id"] == student["incompleted_quizzes"]
