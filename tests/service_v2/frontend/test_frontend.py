from starlette.testclient import TestClient
import os


class TestFrontEnd:

    def test_signin(self, service_v2_frontend: TestClient):
        response = service_v2_frontend.get("/signin")
        assert response.status_code == 200

    def test_signup(self, service_v2_frontend: TestClient):
        response = service_v2_frontend.get("/signup?user_type=student")
        assert response.status_code == 200

    def test_dashboard(self, service_v2_frontend: TestClient):
        response = service_v2_frontend.get("/dashboard/activities")
        assert response.status_code == 200

    def test_dashboard_classroom(self, service_v2_frontend: TestClient):
        response = service_v2_frontend.get("/dashboard/classroom")
        assert response.status_code == 200

    def test_dashboard_quiz(self, service_v2_frontend: TestClient):
        response = service_v2_frontend.get("/dashboard/quiz/start")
        assert response.status_code == 200

    def test_dashboard_user(self, service_v2_frontend: TestClient):
        response = service_v2_frontend.get("/dashboard/user/me")
        assert response.status_code == 200
