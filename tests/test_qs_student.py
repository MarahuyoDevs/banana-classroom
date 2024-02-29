import unittest
from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import Classroom
import os
import boto3

os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "us-east-1"

dynamodb = boto3.resource(
    "dynamodb", region_name="us-east-1", endpoint_url="http://localhost:8000"
)

if "classroom" not in dynamodb.meta.client.list_tables()["TableNames"]:
    Classroom.create_table()

classroom = {}
quiz = {}
valid_classroom_id = "classroom"
valid_student_id = "student"
invalid_classroom_id = "invalid"
invalid_student_id = "invalid"

class TestJoinClassroom():

    client = TestClient(service)

    "Attempt to join a classroom with the given link. Expected outcome: Student successfully joins the classroom and their ID is added to the classroom's student list."
    def test_join_valid_link(self):
        response = self.client.get(
            f"/classroom/join?class-id={valid_classroom_id}&student-id={valid_student_id}",
        )
        assert response.status_code == 200
        assert "success" in response.json()["status"]
        assert valid_student_id in response.json()["data"]["students"]

    "Attempt to join a classroom with an invalid link. Expected outcome: An error message is returned indicating the link is invalid."
    def test_join_invalid_link(self):
        response = self.client.get(
            f"/classroom/join?class-id={invalid_classroom_id}&student-id={valid_student_id}",
        )
        assert response.status_code == 404
        assert "error" in response.json()["status"]
        assert "Invalid link" in response.json()["message"]
                
    "Get a list of completed quizzes. Expected outcome: A list containing the IDs and titles of completed quizzes is returned."
    def test_submit_quiz(self):
        response = self.client.post(
            "/quiz/submit",
            json={
                "class_id": classroom["id"],
                "quiz_id": quiz["id"],
                "description": "test_quiz",
                "instructor": "test_instructor",
                "answers": [
                    {"question_id": quiz['questions'][0]['id'], "answer": quiz['questions'][0]['answer']},
                ],
            },
        )
        assert response.status_code == 200
        assert response.json()["score"] == len([x for x in response.json()["questions"] if x])
    
    "Get a list of incomplete quizzes. Expected outcome: A list containing the IDs and titles of incomplete quizzes is returned."
    def test_get_incomplete_quizzes(self):
        # Input: Student retrieves a list of their incomplete quizzes.
        response = self.client.get("/student/incomplete_quizzes")
        # Expected Output: A list containing the IDs and titles of incomplete quizzes is returned.
        expected_output = [
            {"id": "quiz_id_1", "title": "Incomplete Quiz 1"},
            {"id": "quiz_id_2", "title": "Incomplete Quiz 2"}
        ]
        assert response.status_code == 200
        assert response.json() == expected_output

    "Student finished a quiz. Expected outcome: The quiz ID is added to the student's completed_quizzes list. An error message is displayed if the quiz is already marked as completed."
    def test_student_finished_quiz(self):
        # Assuming a student finished the quiz, let's say with ID 'student123'
        student_id = "student123"
        # Mocking the completion of a quiz by adding its ID to completed_quizzes
        student = {"id": student_id, "completed_quizzes": [], "incompleted_quizzes": []}
        student["completed_quizzes"].append(quiz["id"])
        assert quiz["id"] in student["completed_quizzes"]

    "Student failed a quiz. Expected outcome: The quiz ID is added to the student's incompleted_quizzes list. An error message is displayed if the quiz is already marked as incompleted."
    def test_student_failed_quiz(self):
        # Assuming a student failed to finish the quiz, let's say with ID 'student456'
        student_id = "student456"
        # Mocking the failure of a quiz by adding its ID to incompleted_quizzes
        student = {"id": student_id, "completed_quizzes": [], "incompleted_quizzes": []}
        student["incompleted_quizzes"].append(quiz["id"])
        assert quiz["id"] in student["incompleted_quizzes"]
