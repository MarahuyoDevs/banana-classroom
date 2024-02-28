from starlette.testclient import TestClient
import boto3
from jose import jwt
import os
from banana_classroom.services.user_service.databases.NOSQL.userNOSQL import (
    User,
)
from banana_classroom.services.user_service.app import service


os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "us-east-1"

import boto3

dynamodb = boto3.resource(
    "dynamodb", region_name="us-east-1", endpoint_url="http://localhost:8000"
)

if "user" not in dynamodb.meta.client.list_tables()["TableNames"]:
    User.create_table()


class TestService:

    client = TestClient(
        service, base_url="http://testserver/", headers={"Authorization": "Bearer 123"}
    )
    user = {}

    def test_post(self):
        response = self.client.post(
            "/",
            json={
                "name": "John Doe",
                "email": "johndoe@gmail.com",
                "password": "password",
            },
        )
        assert response.status_code == 200
        self.user.setdefault("id", response.json()["id"])

    def test_get(self):
        response = self.client.get("/me/", headers={"user-id": self.user["id"]})
        assert response.status_code == 200
        self.user.update(response.json())

    def test_put(self):
        self.user.update({"name": "Jane Doe"})
        response = self.client.put(
            "/me/", json=self.user, headers={"user-id": self.user["id"]}
        )
        assert response.status_code == 200
        self.user.update(response.json())

    def test_delete(self):
        response = self.client.delete("/me/", headers={"user-id": self.user["id"]})
        assert response.status_code == 200
