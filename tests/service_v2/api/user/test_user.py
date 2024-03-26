from typing import Callable
from faker import Faker
from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import User
from datetime import datetime


class TestUser:

    my_user = {}

    def test_create_user(self, service_v2_client: TestClient, create_user: Callable):
        user, *_ = create_user("student")
        self.my_user["dummy"] = user
        response = service_v2_client.post(
            f"/user/create?user_type={user.role}",
            json={
                **{
                    "input-password": user.password,
                    **user.model_dump(exclude={"created_at", "updated_at"}),
                },
                "input-confirm-password": user.password,
            },
        )
        assert response.status_code == 201
        assert response.text == "User created successfully"

    def test_read_user(
        self, service_v2_authenticated_client: Callable[[User], TestClient]
    ):
        response = service_v2_authenticated_client(self.my_user["dummy"]).get(
            "/user/me/"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == self.my_user["dummy"].email
        assert data["name"] == self.my_user["dummy"].name
        assert data["role"] == self.my_user["dummy"].role
        assert "password" not in data

    def test_update_user(
        self, service_v2_authenticated_client: Callable[[User], TestClient]
    ):
        fake = Faker()
        new_name = fake.name()
        response = service_v2_authenticated_client(self.my_user["dummy"]).put(
            "/user/me/",
            headers={"email": self.my_user["dummy"].email},
            json={"name": new_name},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == self.my_user["dummy"].email
        assert data["name"] == new_name
        assert data["role"] == self.my_user["dummy"].role
        assert "password" not in data

    def test_delete_user(
        self, service_v2_authenticated_client: Callable[[User], TestClient]
    ):
        response = service_v2_authenticated_client(self.my_user["dummy"]).delete(
            "/user/me/"
        )
        assert response.status_code == 204
