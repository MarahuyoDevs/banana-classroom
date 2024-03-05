from starlette.testclient import TestClient


class TestFrontEnd:

    def test_signin(self, service_v2_frontend_client: TestClient):
        response = service_v2_frontend_client.get("/signin")
        assert response.status_code == 200
        assert response.json() == {"message": "Sign in"}

    def test_signup(self, service_v2_frontend_client: TestClient):
        response = service_v2_frontend_client.get("/signup")
        assert response.status_code == 200
        assert response.json() == {"message": "Sign up"}

    def test_dashboard(self, service_v2_frontend_client: TestClient):
        response = service_v2_frontend_client.get("/dashboard")
        assert response.status_code == 200
        assert response.json() == {"message": "Dashboard"}

    def test_dashboard_classroom(self, service_v2_frontend_client: TestClient):
        response = service_v2_frontend_client.get("/dashboard/classroom")
        assert response.status_code == 200
        assert response.json() == {"message": "Classroom"}

    def test_dashboard_quiz(self, service_v2_frontend_client: TestClient):
        response = service_v2_frontend_client.get("/dashboard/quiz")
        assert response.status_code == 200
        assert response.json() == {"message": "Quiz"}

    def test_dashboard_user(self, service_v2_frontend_client: TestClient):
        response = service_v2_frontend_client.get("/dashboard/profile")
        assert response.status_code == 200
        assert response.json() == {"message": "User"}
