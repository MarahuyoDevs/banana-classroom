from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import Classroom
from datetime import datetime
from starlette import status

class TestClassroom:
    def test_create_classroom(self, service_v2_client: TestClient):
        classroom = Classroom(
            name="Test Classroom",
            description="This is a test classroom",
            instructor="instructor@email.com",
            students=["student1@email.com", "student2@email.com"],
            created_at=str(datetime.now()),
            updated_at=str(datetime.now())
        )
        response = service_v2_client.post("/api/v1/classroom/create", json=classroom.model_dump(exclude={'created_at', 'updated_at'}))
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['name'] == "Test Classroom"
        assert data['description'] == "This is a test classroom"
        assert data['instructor'] == "instructor@email.com"
        assert set(data['students']) == set(["student1@email.com", "student2@email.com"])

    def test_read_classroom(self, service_v2_client: TestClient):
        response = service_v2_client.get("/api/v1/classroom/Test Classroom")
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == "Test Classroom"
        assert data['description'] == "This is a test classroom"
        assert data['instructor'] == "instructor@email.com"
        assert set(data['students']) == set(["student1@email.com", "student2@email.com"])

    def test_update_classroom(self, service_v2_client: TestClient):
        response = service_v2_client.put("/api/v1/classroom/Test Classroom", json={"description": "This is an updated test classroom"})
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == "Test Classroom"
        assert data['description'] == "This is an updated test classroom"
        assert data['instructor'] == "instructor@email.com"
        assert set(data['students']) == set(["student1@email.com", "student2@email.com"])

    def test_delete_classroom(self, service_v2_client: TestClient):
        response = service_v2_client.delete("/api/v1/classroom/Test Classroom")
        assert response.status_code == 204