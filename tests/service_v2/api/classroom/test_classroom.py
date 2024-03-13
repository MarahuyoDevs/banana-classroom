from typing import Callable
from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import Classroom, User


class TestClassroom:

    my_instructor = {}
    my_classroom = {}

    def test_create_classroom(
        self,
        service_v2_authenticated_client: Callable[[User], TestClient],
        create_classroom: Callable[[str, str, User], tuple[Classroom]],
        create_authenticated_user: Callable[[str], User],
    ):

        self.my_instructor.update({"dummy": create_authenticated_user("instructor")})

        self.my_classroom["dummy"] = create_classroom(
            "Information Management", "About Chupa", self.my_instructor["dummy"]
        )[0]

        response = service_v2_authenticated_client(self.my_instructor["dummy"]).post(
            f"/classroom/create/", json=self.my_classroom["dummy"].model_dump()
        )

        assert response.status_code == 201
        assert response.text == "Classroom created successfully"

        self.my_instructor["dummy"] = User.safe_get(
            hash_key=self.my_instructor["dummy"].email
        )
        self.my_instructor["dummy"].password = "mypassword"  # type: ignore

    def test_read_classroom(
        self, service_v2_authenticated_client: Callable[[User], TestClient]
    ):
        response = service_v2_authenticated_client(self.my_instructor["dummy"]).get(
            f"/classroom/find/?id={self.my_instructor['dummy'].classrooms[0]}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == self.my_classroom["dummy"].name
        assert data["description"] == self.my_classroom["dummy"].description

    def test_update_classroom(
        self, service_v2_authenticated_client: Callable[[User], TestClient]
    ):
        response = service_v2_authenticated_client(self.my_instructor["dummy"]).put(
            f"/classroom/update/?id={self.my_instructor['dummy'].classrooms[0]}",
            json={
                "instructor": "Serverns",
                "description": "About Database",
            },
        )
        assert response.status_code == 202
        assert response.text == "Classroom updated successfully"

    def test_delete_classroom(
        self, service_v2_authenticated_client: Callable[[User], TestClient]
    ):
        response = service_v2_authenticated_client(self.my_instructor["dummy"]).delete(
            f"/classroom/delete/?id={self.my_instructor['dummy'].classrooms[0]}"
        )
        assert response.status_code == 204
        assert response.text == "Classroom Information Management deleted"
