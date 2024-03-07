from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import Quiz, Question
from datetime import datetime

class TestQuiz:
    def test_create_quiz(self, service_v2_client: TestClient):
        question1 = Question(
            type="multiple_choice",
            text="Who is the richest man in the Philippines?",
            options=["Bongbong Marcos", "Chavit Singson", "Willie Revillame", "Henry Sy"],
            answer="Bongbong Marcos"
        )
        question2 = Question(
            type="multiple_choice",
            text="Who is the appointed Son of God?",
            options=["Felix Manalo", "Apollo Quiboloy", "Eli Soriano", "Eduardo Manalo"],
            answer="Apollo Quiboloy"
        )
        quiz = Quiz(
            name="Test Quiz",
            description="This is a test quiz",
            questions=[question1, question2],
            created_at=str(datetime.now()),
            updated_at=str(datetime.now())
        )
        response = service_v2_client.post("/api/v1/quiz/create", json=quiz.model_dump(exclude={'created_at', 'updated_at'}))
        assert response.status_code == 201
        data = response.json()
        assert data['name'] == "Test Quiz"
        assert data['description'] == "This is a test quiz"
        assert len(data['questions']) == 2

    def test_read_quiz(self, service_v2_client: TestClient):
        response = service_v2_client.get("/api/v1/quiz/Test Quiz")
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == "Test Quiz"
        assert data['description'] == "This is a test quiz"
        assert len(data['questions']) == 2

    def test_update_quiz(self, service_v2_client: TestClient):
        response = service_v2_client.put("/api/v1/quiz/Test Quiz", json={"description": "This is an updated test quiz"})
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == "Test Quiz"
        assert data['description'] == "This is an updated test quiz"
        assert len(data['questions']) == 2

    def test_delete_quiz(self, service_v2_client: TestClient):
        response = service_v2_client.delete("/api/v1/quiz/Test Quiz")
        assert response.status_code == 204