import pytest
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import Classroom
from starlette import status

# Fixture to create a classroom
@pytest.fixture(scope="module")
def classroom():
    classroom_instance = Classroom(title="Test Classroom", description="Test Description", instructor="Test Instructor")
    classroom_instance.save()
    yield classroom_instance
    classroom_instance.delete()

# Fixture to create a quiz
@pytest.fixture(scope="module")
def quiz(classroom):
    quiz_instance = {"id": "test_quiz_id", "title": "Test Quiz", "description": "Test Quiz Description", "instructor": "Test Instructor"}
    return quiz_instance

# Fixture to provide a test client with set up environment and necessary data
@pytest.fixture(scope="class")
def test_setup(dynamodb, test_client, classroom, quiz):
    yield {"client": test_client, "classroom": classroom}

# Test class
class TestViewQuizResults:

    def test_view_quiz_results_after_submission(self, test_setup):
        test_client = test_setup["client"]
        classroom = test_setup["classroom"]
        quiz = test_setup["quiz"]

        response = test_client.get(
            f"/quiz/results?class-id={classroom.id}&quiz-id={quiz['id']}",
        )
        assert response.status_code == 200

    def test_view_quiz_results_after_submission_failing_score(self, test_setup):
        test_client = test_setup["client"]
        classroom = test_setup["classroom"]
        quiz = test_setup["quiz"]

        response = test_client.get(
            f"/quiz/results?class-id={classroom.id}&quiz-id={quiz['id']}",
        )
        assert response.status_code == 200

    def test_view_quiz_results_before_submission(self, test_setup):
        test_client = test_setup["client"]
        classroom = test_setup["classroom"]
        quiz = test_setup["quiz"]

        response = test_client.get(
            f"/quiz/results?class-id={classroom.id}&quiz-id={quiz['id']}",
        )
        assert response.status_code == 200

    def test_access_private_feedback(self, test_setup):
        test_client = test_setup["client"]
        classroom = test_setup["classroom"]
        quiz = test_setup["quiz"]

        response = test_client.get(
            f"/quiz/results?class-id={classroom.id}&quiz-id={quiz['id']}&student-id=another_student_id",
        )
        assert response.status_code == 403
        assert response.json()["message"] == "Access denied or redirection to own quiz results"

    def test_quiz_result_tampering(self, test_setup):
        test_client = test_setup["client"]
        classroom = test_setup["classroom"]
        quiz = test_setup["quiz"]

        response = test_client.put(
            "/quiz/results",
            json={
                "class_id": classroom.id,
                "quiz_id": quiz['id'],
                "student_id": "student_id",
                "score": 1000,
            },
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json()["message"] == "Quiz result tampering detected"

    def test_large_number_of_questions(self, test_setup):
        test_client = test_setup["client"]
        classroom = test_setup["classroom"]

        response = test_client.get(
            "/quiz/results?class-id={}&quiz-id=large_quiz_id&student-id=student_id".format(classroom.id)
        )
        assert response.status_code == 200
        assert response.json().get("results")
        assert len(response.json()["results"]) > 1
