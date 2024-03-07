from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import User
from datetime import datetime

class TestUser:

    def test_create_user(self, service_v2_client: TestClient):
        user = User(
            name="Vien Kendrick A. Morfe",
            email="kumamoment@gmail.com",
            password="mygoodpassword",
            role="student",
            created_at=str(datetime.now()),
            updated_at=str(datetime.now())
        )
        response = service_v2_client.post("/api/v1/user/create", json=user.model_dump(exclude={'created_at','updated_at'}))
        assert response.status_code == 201
        data = response.json()
        assert data['email'] == "kumamoment@gmail.com"
        assert data['name'] == "Vien Kendrick A. Morfe"
        assert data['role'] == "student"
        assert 'password' not in data

    def test_read_user(self, service_v2_client: TestClient):
        response = service_v2_client.get("/api/v1/user/me/",headers={"email":"kumamoment@gmail.com"})
        assert response.status_code == 200
        data = response.json()
        assert data['email'] == "kumamoment@gmail.com"
        assert data['name'] == "Vien Kendrick A. Morfe"
        assert data['role'] == "student"
        assert 'password' not in data
        
    def test_update_user(self, service_v2_client: TestClient):
        response = service_v2_client.put("/api/v1/user/me/",headers={"email":"kumamoment@gmail.com"}, json={"name":"Vien Kendrick A. Morfe"})
        assert response.status_code == 200
        data = response.json()
        assert data['email'] == "kumamoment@gmail.com"
        assert data['name'] == "Vien Kendrick A. Morfe"
        assert data['role'] == "student"
        assert 'password' not in data

    def test_delete_user(self, service_v2_client: TestClient):
        response = service_v2_client.delete("/api/v1/user/me/", headers={"email":"kumamoment@gmail.com"})
        assert response.status_code == 204