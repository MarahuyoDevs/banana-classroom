from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import Quiz

class TestQuiz:
    
    my_classroom = {}
    my_quiz = {}
    
    def test_create_quiz(self, service_v2_client: TestClient, create_quiz:tuple[Quiz],create_classroom):
        classroom,*_ = create_classroom('GayQuiz','GayQuiz Description')
        classroom.save()
        quiz, *_ = create_quiz(classroom.id)
        response = service_v2_client.post(f"/api/v1/quiz/create", json=quiz.model_dump(exclude={'created_at','updated_at'}))
        assert response.status_code == 201
        assert response.text == "Quiz created successfully"
        self.my_classroom['dummy'] = classroom
        self.my_quiz['dummy'] = quiz

    def test_read_quiz(self, service_v2_client: TestClient):
        response = service_v2_client.get(f"/api/v1/quiz/find?classroom_id={self.my_classroom['dummy'].id}&quiz_id={self.my_quiz['dummy'].id}")
        assert response.status_code == 200
        

    def test_update_quiz(self, service_v2_client: TestClient):
        response = service_v2_client.put(f"/api/v1/quiz/update?classroom_id={self.my_classroom['dummy'].id}&quiz_id={self.my_quiz['dummy'].id}",json={
            "name": "quiz ni bading",
            "description": "chupa",
        })
        assert response.status_code == 202
        assert response.text == "Quiz updated successfully"

    """def test_delete_quiz(self, service_v2_client: TestClient):
        response = service_v2_client.delete(f"/api/v1/quiz/delete?classroom_id={self.my_classroom['dummy'].id}&quiz_id{self.my_quiz['dummy'].id}")
        assert response.status_code == 204
        assert response.text == "Quiz GayQuiz deleted"""