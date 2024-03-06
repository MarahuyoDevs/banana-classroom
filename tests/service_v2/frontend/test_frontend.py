from starlette.testclient import TestClient


class TestFrontEnd:

    def test_signin(self, service_v2_client: TestClient):
        response = service_v2_client.get("/signin")
        assert response.status_code == 200

    def test_signup(self, service_v2_client: TestClient):
        response = service_v2_client.get("/signup")
        assert response.status_code == 200

    def test_dashboard(self, service_v2_client: TestClient):
        response = service_v2_client.get("/dashboard/activities")
        assert response.status_code == 200

    def test_dashboard_classroom(self, service_v2_client: TestClient):
        response = service_v2_client.get("/dashboard/classroom")
        assert response.status_code == 200

    def test_dashboard_quiz(self, service_v2_client: TestClient):
        response = service_v2_client.get("/dashboard/quiz")
        assert response.status_code == 200

    def test_dashboard_user(self, service_v2_client: TestClient):
        response = service_v2_client.get("/dashboard/user/me")
        assert response.status_code == 200
