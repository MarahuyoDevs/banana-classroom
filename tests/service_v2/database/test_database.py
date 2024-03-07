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
    def create(name, email, password, role, created_at, updated_at):
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
    def _create(name, description, questions, created_at, updated_at):
        quiz = Quiz(
            name=name,
            description=description,
            questions=questions,
            created_at=created_at,
            updated_at=updated_at,
        )
        quiz.save()
        return quiz

    return _create


class TestUserTable:
    time = str(datetime.now())

    @pytest.mark.parametrize(
        "name, email, password, role",
        [
            ("vien morfe", "morfevien@gmail.com", "morfe123", "student"),
            ("jane smith", "janesmith@example.com", "password123", "instructor"),
            ("bob johnson", "bobjohnson@test.com", "securepassword", "student"),
        ],
    )
    def test_create_user(self, name, email, password, role):
        user = User(
            name=name,
            email=email,
            password=password,
            role=role,
            created_at=self.time,
            updated_at=self.time,
        )
        assert user.name == name
        assert user.email == email
        assert user.password == password
        assert user.role == role
        assert user.created_at == self.time
        assert user.updated_at == self.time
        user.save()

    @pytest.mark.parametrize(
        "email",
        [
            "morfevien@gmail.com",
            "bergoniomhell@sex.com",
            "alferezkarl@robeck.com",
        ],
    )
    def test_get_user(self, email):
        users = User.query(hash_key=email)
        for user in users:
            assert user.email == email
            
    @pytest.mark.parametrize(
        "email, new_password",
        [
            ("morfevien@gmail.com", "newpassword123"),
            ("bergoniomhell@sex.com", "securepassword456"),
            ("alferezkarl@robeck.com", "changedpassword"),
        ],
    )
    def test_update_user(self, email, new_password):
        new_time = str(datetime.now())
        users = User.query(hash_key=email)
        for user in users:
            user.update(A.password.set(new_password))
            user.update(A.updated_at.set(new_time))
        updated_users = User.query(hash_key=email)

        for user in updated_users:
            assert user.password == new_password
            assert user.updated_at == new_time

    @pytest.mark.parametrize(
        "email",
        [
            "morfevien@gmail.com",
            "janesmith@example.com",
            "bobjohnson@test.com",
        ],
    )
    def test_delete_user(self, email):
        users = User.query(hash_key=email)
        for user in users:
            user.delete()
        deleted_user = User.safe_get(hash_key=email)
        assert not deleted_user


class TestClassroomTable:
    time = str(datetime.now())
    
    @pytest.mark.parametrize(
        "classroom_name, classroom_description, instructor_email, student_emails",
        [
            (
                "Test Classroom 1",
                "Description for Test Classroom 1",
                "teacher1@example.com",
                ["student1@example.com", "student2@example.com"],
            ),
            (
                "Test Classroom 2",
                "Description for Test Classroom 2",
                "teacher2@example.com",
                ["student3@example.com", "student4@example.com"],
            ),
        ],
    )

    def test_create_classroom(self, create_user, classroom_name, classroom_description, instructor_email, student_emails):
        # Create instructor and student users
        instructor = create_user(
            name="Jener Galang",
            email=instructor_email,
            password="chupa123",
            role="instructor",
            created_at=self.time,
            updated_at=self.time,
        )
        students = [
            create_user(
                name=f"Keren {i}",
                email=email,
                password="jabol69",
                role="student",
                created_at=self.time,
                updated_at=self.time,
            )
            for i, email in enumerate(student_emails, start=1)
        ]
        # Create classroom
        classroom = Classroom(
            name=classroom_name,
            description=classroom_description,
            instructor=instructor.email,
            students=[student.email for student in students],
            created_at=self.time,
            updated_at=self.time,
        )
        classroom.save()

        # Assertions
        classroom_db = Classroom.safe_get(hash_key=classroom_name)
        assert classroom_db
        assert classroom_db.name == classroom_name
        assert classroom_db.description == classroom_description
        assert classroom_db.instructor == instructor.email
        assert set(classroom_db.students) == set(student.email for student in students)

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

    @pytest.mark.parametrize(
        "name, description, questions",
        [
            (
                "Test Quiz 1",
                "Test Description 1",
                [
                    {
                        "question": "Richest Man in Philippines",
                        "options": [
                            "Blengblong Marcos",
                            "Willie Revillame",
                            "Henry Sy",
                            "Enrique Razon Jr",
                        ],
                        "answer": "Enrique Razon Jr",
                    },
                    {
                        "question": "Appointed Son of God",
                        "options": ["Apollo Quiboloy", "Eduardo Manalo", "Eli Soriano", "Felix Manalo"],
                        "answer": "Apollo Quiboloy",
                    },
                ],
            ),
        ],
    )    

    def test_create_quiz(self, create_quiz, name, description, questions):
        quiz = create_quiz(
            name=name,
            description=description,
            questions=questions,
            created_at=self.time,
            updated_at=self.time,
        )

        quiz_db = Quiz.safe_get(hash_key=name)
        assert quiz_db
        assert quiz_db.name == name
        assert quiz_db.description == description
        assert quiz_db.questions == questions
        assert quiz_db.created_at == self.time
        assert quiz_db.updated_at == self.time

        
    def test_read_quiz(self, create_quiz):
        quiz = Quiz.safe_get(hash_key="Test Quiz")
        assert quiz
        assert quiz.name == "Test Quiz"
        assert quiz.description == "Test Description"

    @pytest.mark.parametrize(
        "quiz_name, new_description",
        [
            ("Test Quiz 1", "Updated description for Test Quiz 1"),
            ("Test Quiz 2", "Updated description for Test Quiz 2"),
        ],
    )
    def test_update_quiz(self, create_quiz, quiz_name, new_description):
        quiz = Quiz.safe_get(hash_key=quiz_name)
        new_time = str(datetime.now())
        assert quiz
        quiz.update(A.description.set(new_description))
        quiz.update(A.updated_at.set(new_time))
        updated_quiz = Quiz.safe_get(hash_key=quiz_name)
        assert updated_quiz
        assert updated_quiz.description == new_description
        assert updated_quiz.updated_at == new_time

    @pytest.mark.parametrize(
        "quiz_name",
        [
            "Test Quiz 1",
            "Test Quiz 2",
        ],
    )
    def test_delete_quiz(self, create_quiz, quiz_name):
        quiz = Quiz.safe_get(hash_key=quiz_name)
        assert quiz
        quiz.delete()
        deleted_quiz = Quiz.safe_get(hash_key=quiz_name)
        assert not deleted_quiz
        
