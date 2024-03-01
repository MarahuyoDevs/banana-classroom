import unittest
from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)
import os
import boto3

os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"

dynamodb = boto3.resource(
    "dynamodb", region_name="ap-southeast-1", endpoint_url="http://localhost:8000"
)

if "classroom" not in dynamodb.meta.client.list_tables()["TableNames"]:
    Classroom.create_table()

classroom = {}
quiz = {}


class TestViewQuizResults:

    client = TestClient(service)

    def test_view_quiz_results_after_submission(self):
        response = self.client.get(
            f"/quiz/results?class-id={classroom['id']}&quiz-id={quiz['id']}",
        )
        assert response.status_code == 200

    def test_view_quiz_results_after_submission_failing_score(self):
        response = self.client.get(
            f"/quiz/results?class-id={classroom['id']}&quiz-id={quiz['id']}",
        )
        assert response.status_code == 200

    def test_view_quiz_results_before_submission(self):
        response = self.client.get(
            f"/quiz/results?class-id={classroom['id']}&quiz-id={quiz['id']}",
        )
        assert response.status_code == 200

    def test_access_private_feedback(self):
        response = self.client.get(
            "/quiz/results?class-id={}&quiz-id={}&student-id={}".format(
                classroom["id"], quiz["id"], "another_student_id"
            )
        )
        assert response.status_code == 403
        assert (
            response.json()["message"]
            == "Access denied or redirection to own quiz results"
        )

    def test_quiz_result_tampering(self):
        response = self.client.put(
            "/quiz/results",
            json={
                "class_id": classroom["id"],
                "quiz_id": quiz["id"],
                "student_id": "student_id",
                "score": 1000,  # Attempt to modify the score
            },
        )
        assert response.status_code == 400  # Or whatever appropriate status code
        assert response.json()["message"] == "Quiz result tampering detected"

    def test_large_number_of_questions(self):
        # Assuming a quiz with large number of questions is already created
        # Simulate accessing quiz results for that quiz
        response = self.client.get(
            "/quiz/results?class-id={}&quiz-id={}&student-id={}".format(
                classroom["id"], "large_quiz_id", "student_id"
            )
        )
        assert response.status_code == 200
        assert response.json().get("results")
        assert len(response.json()["results"]) > 0


if __name__ == "__main__":
    unittest.main()
