import datetime
from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import Classroom
import os
import boto3

os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "us-east-1"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ["DYNTASTIC_REGION"],
    endpoint_url=os.environ["DYNTASTIC_HOST"],
)

if "classroom" not in dynamodb.meta.client.list_tables()["TableNames"]:
    Classroom.create_table()

classroom = {}
quiz = {}


class TestClassroom:

    client = TestClient(service)

    def test_post_classroom(self):
        response = self.client.post(
            "/classroom",
            json={
                "title": "test_classroom",
                "description": "test_description",
                "instructor": "test_instructor",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "test_classroom"
        assert response.json()["data"]["description"] == "test_description"
        assert response.json()["data"]["instructor"] == "test_instructor"
        classroom.setdefault("id", response.json()["data"]["id"])

    def test_get_classroom(self):
        response = self.client.get(f"/classroom/{classroom['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == "test_classroom"
        assert response.json()["description"] == "test_description"
        assert response.json()["instructor"] == "test_instructor"

    def test_put_classroom(self):
        response = self.client.put(
            f"/classroom/{classroom['id']}",
            json={
                "title": "test_classroom_updated",
                "description": "test_description_updated",
                "instructor": "test_instructor_updated",
            },
        )
        assert response.status_code == 200
        assert response.json()["title"] == "test_classroom_updated"
        assert response.json()["description"] == "test_description_updated"
        assert response.json()["instructor"] == "test_instructor_updated"

    """def test_delete_classroom(self):
        response = self.client.delete(f"/classroom/{classroom['id']}")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["id"] == classroom["id"]"""


class TestQuiz:

    client = TestClient(service)

    def test_quiz_create(self):
        time = datetime.datetime.now().isoformat()
        response = self.client.post(
            "/quiz/create",
            json={
                "title": "test_quiz",
                "description": "test_description",
                "instructor": "test_instructor",
                "class_id": classroom["id"],
                "questions": [
                    {
                        "description": "test_question",
                        "options": ["test_answer", "test_answer", "test_answer"],
                        "answer": "test_answer",
                    }
                ],
                "expiration_time": time,
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "test_quiz"
        assert response.json()["data"]["id"]
        assert response.json()["data"]["expiration_time"] == time
        quiz.update(response.json()["data"])

    def test_join_quiz(self):
        response = self.client.get(
            f"/quiz/join?class-id={classroom["id"]}&quiz-id={quiz["id"]}",
        )
        assert response.status_code == 200
        assert set(response.json()[0].keys()) == {'description','options','answer','id'}
                
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
