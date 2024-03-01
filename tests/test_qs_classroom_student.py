from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import Classroom
from starlette import status
import os
import boto3

os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"

dynamodb = boto3.resource(
    "dynamodb", region_name="ap-southeast-1", endpoint_url="http://localhost:8000"
)

if "classroom" not in dynamodb.meta.client.list_tables()["TableNames"]:
    Classroom.create_table()

class TestClassroomStudentManagement:

    client = TestClient(service)

    "Adding a student to an existing class. Expected output: Student is successfully added to the class roster"
    def test_add_student_to_class(self):
        # Create a classroom
        response = self.client.post(
            "/classroom",
            json={
                "title": "Math Class",
                "description": "Learn math concepts",
                "instructor": "Ms. Johnson",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        classroom_id = response.json()["data"]["id"]

        # Add a student to the class
        response = self.client.post(
            f"/classroom/{classroom_id}/add_student",
            json={"student_id": "123456", "student_name": "John Doe"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "John Doe" in response.json()["data"]["students"]

    "Removing a student from an existing class. Expected output: Student is removed from the class roster"
    def test_remove_student_from_class(self):
        # Create a classroom and add a student
        response = self.client.post(
            "/classroom",
            json={
                "title": "Math Class",
                "description": "Learn math concepts",
                "instructor": "Ms. Johnson",
                "students": ["123456"]
            },
        )
        assert response.status_code == status.HTTP_200_OK
        classroom_id = response.json()["data"]["id"]

        # Remove the student from the class
        response = self.client.post(
            f"/classroom/{classroom_id}/remove_student",
            json={"student_id": "123456"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "123456" not in response.json()["data"]["students"]

    "Adding a student who is already enrolled in the class. Expected output: Notification that the student is already part of the class roster and no action is taken."
    def test_add_student_already_in_class(self):
        # Assume we have a classroom with a student already enrolled
        classroom_id = "example_classroom_id"
        student_id = "existing_student_id"
        classroom = Classroom(
            id=classroom_id,
            title="Sample Class",
            description="Sample description",
            instructor="Sample Instructor",
            students=[student_id]  # Assume the student is already enrolled
        )
        classroom.save()
        
        # Attempt to add the same student again
        response = self.client.put(
            f"/classroom/{classroom_id}/add_student",
            json={"student_id": student_id}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"message": "Student is already part of the class roster"}

    "Removing a student who is not enrolled in the class. Expected output: Notification that the student is not found in the class roster, and no action is taken."
    def test_remove_nonexistent_student(self):
        # Assume we have a classroom with no students enrolled
        classroom_id = "example_classroom_id"
        classroom = Classroom(
            id=classroom_id,
            title="Sample Class",
            description="Sample description",
            instructor="Sample Instructor"
        )
        classroom.save()
        
        # Attempt to remove a student who is not enrolled
        response = self.client.put(
            f"/classroom/{classroom_id}/remove_student",
            json={"student_id": "nonexistent_student_id"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"message": "Student not found in the class roster"}

    "Adding a student with completed and incompleted quizes. Expected output: Student object created with completed and incompleted quizes"
    def test_add_student_with_completed_quizzes(self, setup_classroom):
        classroom_id = setup_classroom
        student_id = "test_student_id"
        completed_quizzes = ["quiz1", "quiz2"]  # Sample completed quizzes
        
        response = self.client.post(
            f"/classroom/{classroom_id}/student",
            json={
                "id": student_id,
                "name": "Test Student",
                "completed_quizzes": completed_quizzes,
                "incompleted_quizzes": [],
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["id"] == student_id
        assert response.json()["data"]["completed_quizzes"] == completed_quizzes
        assert response.json()["data"]["incompleted_quizzes"] == []

    "Removing a student with completed and incompleted quizes. Expected output: Student object created with completed and incompleted quizes"
    def test_remove_student_with_completed_quizzes(self, setup_classroom):
        classroom_id = setup_classroom
        student_id = "test_student_id"
        completed_quizzes = ["quiz1", "quiz2"]  # Sample completed quizzes

        # Add student with completed quizzes
        self.client.post(
            f"/classroom/{classroom_id}/student",
            json={
                "id": student_id,
                "name": "Test Student",
                "completed_quizzes": completed_quizzes,
                "incompleted_quizzes": [],
            },
        )

        # Remove student
        response = self.client.delete(
            f"/classroom/{classroom_id}/student/{student_id}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["id"] == student_id
        assert response.json()["data"]["completed_quizzes"] == completed_quizzes
        assert response.json()["data"]["incompleted_quizzes"] == []