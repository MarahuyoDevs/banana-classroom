from typing import Callable
from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import Classroom, Quiz, User


class TestQuiz:

    my_instructor = {}
    my_classroom = {}
    my_quiz = {}

    def test_create_quiz(
        self,
        service_v2_authenticated_client: Callable[[User], TestClient],
        create_quiz: Callable[[str], tuple[Quiz, str, str]],
        create_authenticated_user: Callable[[str], User],
        create_classroom: Callable[[str, str, User], tuple[Classroom, str, str]],
    ):

        self.my_instructor.update({"dummy": create_authenticated_user("instructor")})

        self.my_classroom.update(
            {
                "dummy": create_classroom(
                    "GayQuiz", "GayQuiz Description", self.my_instructor["dummy"]
                )[0]
            }
        )
        response = service_v2_authenticated_client(self.my_instructor["dummy"]).post(
            "/api/v1/classroom/create",
            json=self.my_classroom["dummy"].model_dump(),
        )

        self.my_instructor["dummy"] = User.safe_get(
            hash_key=self.my_instructor["dummy"].email
        )

        self.my_instructor["dummy"].password = "mypassword"  # type: ignore

        assert self.my_instructor["dummy"]

        self.my_quiz.update(
            {"dummy": create_quiz(self.my_instructor["dummy"].classrooms[0])[0]}
        )
        response = service_v2_authenticated_client(self.my_instructor["dummy"]).post(
            f"/api/v1/quiz/create/?classroom_id={self.my_instructor['dummy'].classrooms[0]}",
            json=self.my_quiz["dummy"].model_dump(exclude={"created_at", "updated_at"}),
        )
        assert response.status_code == 201

    def test_read_quiz(
        self, service_v2_authenticated_client: Callable[[User], TestClient]
    ):
        response = service_v2_authenticated_client(self.my_instructor["dummy"]).get(
            f"/api/v1/quiz/find/?classroom_id={self.my_classroom['dummy'].id}&quiz_id={self.my_quiz['dummy'].id}"
        )
        assert response.status_code == 200
        assert "questions" not in response.json().keys()

    def test_update_quiz(self, service_v2_client: TestClient):
        response = service_v2_client.put(
            f"/api/v1/quiz/update/?classroom_id={self.my_classroom['dummy'].id}&quiz_id={self.my_quiz['dummy'].id}",
            json={
                "name": "quiz ni bading",
                "description": "chupa",
            },
        )
        assert response.status_code == 202
        assert response.text == "Quiz updated successfully"

    def test_delete_quiz(
        self, service_v2_authenticated_client: Callable[[User], TestClient]
    ):
        response = service_v2_authenticated_client(self.my_instructor["dummy"]).delete(
            f"/api/v1/quiz/delete/?id={self.my_quiz['dummy'].id}"
        )
        assert response.status_code == 204
        assert response.text == "Quiz deleted"
