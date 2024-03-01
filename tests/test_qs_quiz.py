from starlette.testclient import TestClient
from banana_classroom.services.quiz_api.quiz_service.app import service
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import Classroom, Quiz
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

class TestQuizCreation:

    client = TestClient(service)

    "Creating a quiz with valid data and questions. Expected output: Quiz object created with questions"
    def test_create_quiz_valid_data(self):
        response_create_quiz = self.client.post(
            "/quiz",
            json={
                "title": "Math Quiz",
                "description": "Test your math skills",
                "instructor": "Mr. Brown",
                "questions": [
                    {
                        "description": "What is the capital of France?",
                        "options": ["Paris", "London", "Berlin"],
                        "answer": "Paris",
                    },
                    {
                        "description": "2 + 2 = ?",
                        "options": ["1", "2", "4"],
                        "answer": "4",
                    },
                ],
            },
        )
        assert response_create_quiz.status_code == status.HTTP_200_OK
        assert response_create_quiz.json()["data"]["title"] == "Math Quiz"
        assert len(response_create_quiz.json()["data"]["questions"]) == 2

    "Creating a quiz with valid data but without questions. Expected output: Quiz object created successfully"
    def test_create_quiz_valid_data_no_questions(self):         
        response = self.client.post(
            "/quiz",
            json={
                "title": "Test Quiz",
                "description": "This is a test quiz",
                "instructor": "John Doe",
                "questions": [] 
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["title"] == "Test Quiz"
        assert response.json()["data"]["description"] == "This is a test quiz"
        assert response.json()["data"]["instructor"] == "John Doe"
        assert response.json()["data"]["questions"] == []

    "Creating a quiz with missing mandatory fields. Expected output: Validation error"
    def test_create_quiz_missing_mandatory_fields(self):
        response = self.client.post(
            "/quiz",
            json={
                "title": "Test Quiz"
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "description" in response.json()["detail"]

    "Creating a quiz with duplicate questions. Expected output: Validation error"
    def test_create_quiz_with_duplicate_questions(test_client):
        quiz_data = {
            "title": "Duplicate Questions Quiz",
            "description": "Quiz with duplicate questions",
            "instructor": "Ms. Davis",
            "questions": [
                {"description": "What is 1 + 1?", "options": ["1", "2", "3"], "answer": "2"},
                {"description": "What is 2 + 2?", "options": ["2", "3", "4"], "answer": "4"},
                {"description": "What is 1 + 1?", "options": ["1", "2", "3"], "answer": "2"}
            ]
        }

        response = test_client.post("/create-quiz", json=quiz_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Questions must be unique" in response.json()["detail"]

    "Adding a new question to an existing quiz. Expected output: Question added to the quiz successfully"
    def test_add_valid_question_to_existing_quiz(self, create_quiz):
        # Given an existing quiz and a new question
        quiz_id = create_quiz
        new_question_data = {
            "description": "What is the capital of France?",
            "options": ["London", "Paris", "Berlin", "Rome"],
            "answer": "Paris"
        }
        # When adding the new question to the existing quiz
        response = self.client.post(f"/quiz/{quiz_id}/question", json=new_question_data)
        # Then the question should be successfully added to the quiz
        assert response.status_code == status.HTTP_200_OK
        updated_quiz = Quiz.get(quiz_id)
        assert len(updated_quiz.questions) == 1
        assert updated_quiz.questions[0].description == "What is the capital of France?"

    "Adding a new question to an existing quiz with missing required fields. Expected output: Validation error"
    def test_add_question_with_missing_required_field(self, create_quiz):
        # Given an existing quiz and a new question with missing required fields
        quiz_id = create_quiz
        new_question_data = {
            "description": "What is the capital of Germany?",
            "options": ["London", "Paris", "Berlin"],  # Missing the answer field
        }
        # When attempting to add the new question to the existing quiz
        response = self.client.post(f"/quiz/{quiz_id}/question", json=new_question_data)
        # Then the operation should fail and an informative message should be returned
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "answer" in response.text
        
    "Modifying quiz title with valid data. Expected output: Quiz title updated successfully"
    def test_modify_quiz_title(self):
        # Create a quiz
        response = self.client.post(
            "/quiz",
            json={
                "title": "Math Quiz",
                "description": "Test your math skills",
                "instructor": "Mr. Smith",
                "questions": [
                    {"description": "What is 2 + 2?", "answer": "4"},
                    {"description": "What is 5 * 5?", "answer": "25"}
                ]
            },
        )
        quiz_id = response.json()["data"]["id"]
        
        # Modify quiz title
        new_title = "Math Quiz Updated"
        response = self.client.put(
            f"/quiz/{quiz_id}/modify_title",
            json={"title": new_title}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["title"] == new_title

    "Modifying quiz description with valid data. Expected output: Quiz description updated successfully"
    def test_modify_quiz_description(self):
        # Create a quiz
        response = self.client.post(
            "/quiz",
            json={
                "title": "History Quiz",
                "description": "Test your knowledge of historical events",
                "instructor": "Ms. Johnson",
                "questions": [
                    {"description": "When was the Declaration of Independence signed?", "answer": "1776"},
                    {"description": "Who was the first president of the United States?", "answer": "George Washington"}
                ]
            },
        )
        quiz_id = response.json()["data"]["id"]
        
        # Modify quiz description
        new_description = "Test your knowledge of world history"
        response = self.client.put(
            f"/quiz/{quiz_id}/modify_description",
            json={"description": new_description}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["description"] == new_description
