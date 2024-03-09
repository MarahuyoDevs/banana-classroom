from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import Classroom

class TestClassroom:
    def test_create_classroom(self, service_v2_client: TestClient,create_classroom:tuple[Classroom]):
        classroom, *_ = create_classroom('Information Management','About Chupa')
        response = service_v2_client.post(f"/api/v1/classroom/create", json=classroom.model_dump())
        assert response.status_code == 201
        assert response.text == "Classroom created successfully"

    def test_read_classroom(self, service_v2_client: TestClient):
        response = service_v2_client.get(f"/api/v1/classroom/find?classroom_name=Information Management")
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == 'Information Management'
        assert data['description'] == 'About Chupa'
        
    def test_update_classroom(self, service_v2_client: TestClient):
        response = service_v2_client.put(f"/api/v1/classroom/update?classroom_name=Information Management",json={
            "instructor": "Serverns",
            "description": "About Database",
        })
        assert response.status_code == 202
        assert response.text == "Classroom updated successfully"
 
    def test_delete_classroom(self, service_v2_client: TestClient):
        response = service_v2_client.delete(f"/api/v1/classroom/delete?classroom_name=Information Management")
        assert response.status_code == 204
        assert response.text == "Classroom Information Management deleted"