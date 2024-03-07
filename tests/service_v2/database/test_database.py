import os
from faker import Faker
from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import (
    User,
    Classroom,
    Quiz,
    Question,
)
import pytest
from datetime import datetime
import boto3
from dyntastic import A

from tests.service_v2.conftest import create_user

os.environ["DYNTASTIC_HOST"] = "http://localhost:8000"
os.environ["DYNTASTIC_REGION"] = "ap-southeast-1"


class TestUserTable:  # Test cases for the User table.
    time = str(datetime.now())

    @pytest.mark.parametrize(
        "name, email, password, role",
        [
            ("vien morfe", "morfevien@gmail.com", "morfe123", "student"),
            ("jane smith", "janesmith@example.com", "password123", "instructor"),
            ("bob johnson", "bobjohnson@test.com", "securepassword", "student"),
        ],
    )
    def test_create_user(self, name: str, email: str, password: str, role: str):
        """Test case to create a new user with valid data.
        Args:
          name (str): Name of the user.
          email (str): Email of the user.
          password (str): Password of the user.
          role (str): Role of the user (student or instructor)."""
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
        """Test case to retrieve a user by email.
        Args:   email (str): Email of the user to retrieve."""
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
        """Test case to update a user's password.
        Args:
            email (str): Email of the user to update.
            new_password (str): New password to set."""
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
        """Test case to delete a user.
        Args:   email (str): Email of the user to delete."""
        users = User.query(hash_key=email)
        for user in users:
            user.delete()
        deleted_user = User.safe_get(hash_key=email)
        assert not deleted_user


class TestClassroomTable:  # Test cases for the Classroom table.

    time = str(datetime.now())

    def test_create_classroom(self, create_user):
        """Test case to create a new classroom.
        Args:
            create_user (function): Fixture to create a user.
            classroom_name (str): Name of the classroom.
            classroom_description (str): Description of the classroom.
            instructor_email (str): Email of the instructor.
            student_emails (list): List of student emails."""
        # Create instructor and student users
        fake = Faker()

        instructor, *_ = create_user("instructor")
        # Create classroom
        classroom = Classroom(
            name="Dummy Classroom",
            description="Dummy description",
            instructor=instructor.email,
            created_at=self.time,
            updated_at=self.time,
        )

        students = []
        for _ in range(5):
            student, *_ = create_user("student")
            students.append(student.email)

        classroom.students = students

        classroom.save()

        classroom_db = Classroom.safe_get(hash_key="Dummy Classroom")
        assert classroom_db
        assert classroom_db.name == "Dummy Classroom"
        assert classroom_db.description == "Dummy description"
        assert classroom_db.instructor == instructor.email
        assert set(classroom_db.students) == set(students)

    def test_read_classroom(self, create_user):
        """Test case to read a classroom.
        Args:   create_user (function): Fixture to create a user."""
        classroom = Classroom.safe_get(hash_key="Dummy Classroom")

        assert classroom
        assert classroom.name == "Dummy Classroom"
        assert classroom.description == "Dummy description"

    def test_update_classroom(self, create_user):
        """Test case to update a classroom.
        Args:  create_user (function): Fixture to create a user."""
        classroom = Classroom.safe_get(hash_key="Dummy Classroom")
        new_instructor, *_ = create_user("instructor")
        assert classroom
        classroom.update(A.description.set("new description for classroom"))
        classroom.update(A.instructor.set(new_instructor.email))
        new_classroom = Classroom.safe_get(hash_key="Dummy Classroom")
        assert new_classroom
        assert new_classroom.name == "Dummy Classroom"
        assert new_classroom.description == "new description for classroom"
        assert new_classroom.instructor == new_instructor.email

    def test_delete_classroom(self):
        """Test case to delete a classroom."""
        classroom = Classroom.safe_get(hash_key="Dummy Classroom")
        assert classroom
        classroom.delete()
        classroom = Classroom.safe_get(hash_key="Dummy Classroom")
        assert not classroom


class TestQuizTable:  # Test cases for the Quiz table.
    time = str(datetime.now())
    my_classroom = {}
    my_quiz = {}

    def test_create_quiz(self, create_classroom):
        """Test case to create a new quiz.
        Args:
            create_quiz (function): Fixture to create a quiz.
            name (str): Name of the quiz.
            description (str): Description of the quiz.
            questions (list): List of questions."""
        classroom = create_classroom("Dummy Classroom", "Dummy description")[0]
        classroom.save()
        self.my_classroom["dummy"] = classroom

        quiz = Quiz(
            name="Test Quiz",
            classroom_id=classroom.name,
            description="Test Description",
            created_at=self.time,
            updated_at=self.time,
        )
        quiz.save()

        quiz_db = Quiz.safe_get(hash_key=quiz.id)
        assert quiz_db
        assert quiz_db.name == "Test Quiz"
        assert quiz_db.description == "Test Description"
        assert quiz_db.questions == []
        assert quiz_db.created_at == self.time
        assert quiz_db.updated_at == self.time
        self.my_quiz["dummy"] = quiz_db

    def test_read_quiz(self):
        """Test case to read a quiz.
        Args:   create_quiz (function): Fixture to create a quiz."""
        quiz = Quiz.safe_get(hash_key=self.my_quiz["dummy"].id)
        assert quiz
        assert quiz.name == "Test Quiz"
        assert quiz.description == "Test Description"

    def test_update_quiz(self):
        """Test case to update a quiz.
        Args:
            create_quiz (function): Fixture to create a quiz.
            quiz_name (str): Name of the quiz to update.
            new_description (str): New description for the quiz."""

        quiz = Quiz.safe_get(hash_key=self.my_quiz["dummy"].id)
        new_time = str(datetime.now())
        assert quiz
        quiz.update(A.description.set("Updated description for Test Quiz 2"))
        quiz.update(A.updated_at.set(new_time))
        updated_quiz = Quiz.safe_get(hash_key=self.my_quiz["dummy"].id)
        assert updated_quiz
        assert updated_quiz.description == "Updated description for Test Quiz 2"
        assert updated_quiz.updated_at == new_time

    def test_delete_quiz(self):
        """Test case to delete a quiz.
        Args:
            create_quiz (function): Fixture to create a quiz.
            quiz_name (str): Name of the quiz to delete."""
        quiz = Quiz.safe_get(hash_key=self.my_quiz["dummy"].id)
        assert quiz
        quiz.delete()
        deleted_quiz = Quiz.safe_get(hash_key=self.my_quiz["dummy"].id)
        assert not deleted_quiz


class TestQuestionTable:

    time = str(datetime.now())
    my_quiz = {}
    my_classroom = {}

    def test_create_question(self, create_quiz, create_question):

        classroom = Classroom.safe_get(hash_key="Dummy Classroom")
        assert classroom
        quiz = create_quiz(classroom.name)[0]
        questions = [create_question(quiz.id)[0] for _ in range(5)]
        map(lambda x: x.save(), questions)
        quiz.questions = [question.id for question in questions]
        quiz.save()
        self.my_quiz["dummy"] = quiz
        self.my_classroom["dummy"] = classroom

        quiz_db = Quiz.safe_get(hash_key=quiz.id)
        assert quiz_db
        quiz_db.questions = [question.id for question in questions]
        assert len(quiz_db.questions) == 5

    def test_read_question(self):
        classroom = Classroom.safe_get(hash_key="Dummy Classroom")
        quiz = Quiz.safe_get(hash_key=self.my_quiz["dummy"].id)
        assert classroom
        assert quiz
        questions = [
            Question.safe_get(hash_key=question, range_key=classroom.name)
            for question in quiz.questions
        ]
        assert len(questions) == 5

    def test_update_question(self, create_question):
        classroom = Classroom.safe_get(hash_key="Dummy Classroom")
        quiz = Quiz.safe_get(hash_key=self.my_quiz["dummy"].id)
        assert classroom
        assert quiz
        questions = [create_question(quiz.id)[0] for _ in range(5)]
        map(lambda x: x.save(), questions)
        quiz.questions = [question.id for question in questions]
        quiz.save()
        quiz_db = Quiz.safe_get(hash_key=quiz.id)
        assert quiz_db
        assert len(quiz_db.questions) == 5

    def test_delete_question(self):
        classroom = Classroom.safe_get(hash_key="Dummy Classroom")
        quiz = Quiz.safe_get(hash_key=self.my_quiz["dummy"].id)
        assert classroom
        assert quiz
        quiz.questions = []
        quiz.save()
        quiz_db = Quiz.safe_get(hash_key=quiz.id)
        assert quiz_db
        assert len(quiz_db.questions) == 0
