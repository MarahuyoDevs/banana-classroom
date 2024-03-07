import os
from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import User, Classroom, Quiz
import pytest
from datetime import datetime
import boto3
from dyntastic import A

os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ["DYNTASTIC_REGION"],
    endpoint_url=os.environ["DYNTASTIC_HOST"],
)

if "users" not in dynamodb.meta.client.list_tables()["TableNames"]:
    User.create_table()

if "classrooms" not in dynamodb.meta.client.list_tables()["TableNames"]:
    Classroom.create_table()


@pytest.fixture
def create_user():
    def create(
        name: str,
        email: str,
        password: str,
        role: str,
        created_at: str,
        updated_at: str,
    ):
        user = User(
            name=name,
            email=email,
            password=password,
            role=role,
            created_at=created_at,
            updated_at=updated_at,
        )
        user.save()
        return user

    return create

@pytest.fixture
def create_quiz():
    def create(
        name: str,
        description: str,
        questions: list,
        created_at: str,
        updated_at: str,
    ):
        quiz = Quiz(
            name=name,
            description=description,
            questions=questions,
            created_at=created_at,
            updated_at=updated_at,
        )
        quiz.save()
        return quiz

    return create


class TestUserTable:

    time = str(datetime.now())

    def test_create_user(self):

        user = User(
            name="vien morfe",
            email="morfevien@gmail.com",
            password="morfe123",
            role="student",
            created_at=self.time,
            updated_at=self.time,
        )
        assert user.name == "vien morfe"
        assert user.email == "morfevien@gmail.com"
        assert user.password == "morfe123"
        assert user.role == "student"
        assert user.created_at == self.time
        assert user.updated_at == self.time
        user.save()

    def test_get_user(self):
        users = User.query(hash_key="morfevien@gmail.com")
        for user in users:
            assert user.name == "vien morfe"
            assert user.email == "morfevien@gmail.com"
            assert user.password == "morfe123"
            assert user.role == "student"
            assert user.created_at == self.time
            assert user.updated_at == self.time
        user.save()

    def test_update_user(self):
        new_time = str(datetime.now())
        users = User.query(hash_key="morfevien@gmail.com")
        for user in users:
            user.update(A.password.set("morfelovestite"))
            user.update(A.updated_at.set(new_time))
        morfe = User.query(hash_key="morfevien@gmail.com")

        for info in morfe:
            assert info.name == "vien morfe"
            assert info.email == "morfevien@gmail.com"
            assert info.password == "morfelovestite"
            assert info.role == "student"
            assert info.created_at == self.time
            assert info.updated_at == new_time

    def test_delete_user(self):
        users = User.query(hash_key="morfevien@gmail.com")
        for user in users:
            user.delete()
        morfe = User.safe_get(hash_key="morfevien@gmail.com")
        assert not morfe


class TestClassroomTable:
    time = str(datetime.now())

    def test_create_classroom(self, create_user):
        # user
        instructor = create_user(
            name="vien morfe",
            email="morfevien@gmail.com",
            password="morfe123",
            role="instructor",
            created_at=self.time,
            updated_at=self.time,
        )
        instructor_db = User.safe_get(hash_key="morfevien@gmail.com")
        assert instructor_db
        assert instructor_db.name == instructor.name
        assert instructor_db.email == instructor.email
        assert instructor_db.password == instructor.password
        assert instructor_db.role == instructor.role
        assert instructor_db.created_at == instructor.created_at
        assert instructor_db.updated_at == instructor.updated_at

        student1 = create_user(
            name="vien1 morfe",
            email="morfevien1@gmail.com",
            password="morfe123",
            role="student",
            created_at=self.time,
            updated_at=self.time,
        )
        student2 = create_user(
            name="vien2 morfe",
            email="morfevien2@gmail.com",
            password="morfe123",
            role="student",
            created_at=self.time,
            updated_at=self.time,
        )
        users = [x for x in User.scan(A.role == "student")]  # type: ignore
        assert len(users) == 2

        classroom = Classroom(
            name="test classroom",
            description="test classroom description",
            instructor=instructor.email,
            students=[student1.email, student2.email],
            created_at=self.time,
            updated_at=self.time,
        )
        classroom.save()

        classroom_db = Classroom.safe_get(hash_key="test classroom")
        assert classroom_db
        assert classroom_db.name == classroom.name
        assert classroom_db.description == classroom.description
        assert classroom_db.instructor == classroom.instructor
        assert classroom_db.created_at == classroom.created_at
        assert classroom_db.updated_at == classroom.updated_at
        for student_email in classroom_db.students:
            assert student_email in [student1.email, student2.email]

    def test_read_classroom(self, create_user):
        classroom = Classroom.safe_get(hash_key="test classroom")

        assert classroom
        assert classroom.name == "test classroom"
        assert classroom.description == "test classroom description"
        assert classroom.instructor == "morfevien@gmail.com"

    def test_update_classroom(self, create_user):
        classroom = Classroom.safe_get(hash_key="test classroom")
        new_instructor = create_user(
            name="Mhell Bergonio",
            email="mhellbergonio@gmail.com",
            password="morfe123",
            role="instructor",
            created_at=self.time,
            updated_at=self.time,
        )
        assert classroom
        classroom.update(A.description.set("new description for classroom"))
        classroom.update(A.instructor.set(new_instructor.email))
        new_classroom = Classroom.safe_get(hash_key="test classroom")
        assert new_classroom
        assert new_classroom.name == "test classroom"
        assert new_classroom.description == "new description for classroom"
        assert new_classroom.instructor == new_instructor.email

    def test_delete_classroom(self):
        classroom = Classroom.safe_get(hash_key="test classroom")
        assert classroom
        classroom.delete()
        classroom = Classroom.safe_get(hash_key="test classroom")
        assert not classroom

class TestQuizTable:
    time = str(datetime.now())

    def test_create_quiz(self, create_quiz):
        questions = [
            {
                "question": "Richest Man in Philippines",
                "options": ["Blengblong Marcos", "Willie Revillame", "Henry Sy", "Enrique Razon Jr"],
                "answer": "Enrique Razon Jr",
            },
            {
                "question": "Appointed Son of God",
                "options": ["Apollo Quiboloy", "Eduardo Manalo", "Eli Soriano", "Felix Manalo"],
                "answer": "Apollo Quiboloy",
            },
        ]
        quiz = create_quiz(
            name="Test Quiz",
            description="Test Description",
            questions=questions,
            created_at=self.time,
            updated_at=self.time,
        )

        quiz_db = Quiz.safe_get(hash_key="Test Quiz")
        assert quiz_db
        assert quiz_db.name == quiz.name
        assert quiz_db.description == quiz.description
        assert quiz_db.questions == quiz.questions
        assert quiz_db.created_at == quiz.created_at
        assert quiz_db.updated_at == quiz.updated_at

    def test_read_quiz(self, create_quiz):
        quiz = Quiz.safe_get(hash_key="Test Quiz")
        assert quiz
        assert quiz.name == "Test Quiz"
        assert quiz.description == "Test Description"

    def test_update_quiz(self, create_quiz):
        quiz = Quiz.safe_get(hash_key="Test Quiz")
        new_time = str(datetime.now())
        assert quiz
        new_description = "Updated test description for the test quiz"
        quiz.update(A.description.set(new_description))
        quiz.update(A.updated_at.set(new_time))
        updated_quiz = Quiz.safe_get(hash_key="Test Quiz")
        assert updated_quiz
        assert updated_quiz.name == "Test Quiz"
        assert updated_quiz.description == new_description
        assert updated_quiz.created_at == self.time
        assert updated_quiz.updated_at == new_time

    def test_delete_quiz(self, create_quiz):
        quiz = Quiz.safe_get(hash_key="Test Quiz")
        assert quiz
        quiz.delete()
        deleted_quiz = Quiz.safe_get(hash_key="Test Quiz")
        assert not deleted_quiz
