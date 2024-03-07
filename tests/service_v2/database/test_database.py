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

# Create the 'users' table if it doesn't exist
if "users" not in dynamodb.meta.client.list_tables()["TableNames"]:
    User.create_table()

# Create the 'classrooms' table if it doesn't exist
if "classrooms" not in dynamodb.meta.client.list_tables()["TableNames"]:
    Classroom.create_table()


@pytest.fixture
def create_user():
    """ Fixture to create a user in the database.
    Returns a function that takes name, email, password, role, created_at, and updated_at as arguments and returns a User object. """
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
    """Fixture to create a quiz in the database.
    Returns a function that takes name, description, questions, created_at, and updated_at as arguments and returns a Quiz object."""
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

class TestUserTable: #Test cases for the User table.
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
        """ Test case to create a new user with valid data.
          Args:
            name (str): Name of the user.
            email (str): Email of the user.
            password (str): Password of the user.
            role (str): Role of the user (student or instructor).   """
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
            new_password (str): New password to set.    """
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
        Args:   email (str): Email of the user to delete.   """
        users = User.query(hash_key=email)
        for user in users:
            user.delete()
        deleted_user = User.safe_get(hash_key=email)
        assert not deleted_user


class TestClassroomTable: #Test cases for the Classroom table.
    
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
        """ Test case to create a new classroom.
        Args:
            create_user (function): Fixture to create a user.
            classroom_name (str): Name of the classroom.
            classroom_description (str): Description of the classroom.
            instructor_email (str): Email of the instructor.
            student_emails (list): List of student emails.  """
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
        """ Test case to read a classroom.
        Args:   create_user (function): Fixture to create a user.   """
        classroom = Classroom.safe_get(hash_key="test classroom")

        assert classroom
        assert classroom.name == "test classroom"
        assert classroom.description == "test classroom description"
        assert classroom.instructor == "morfevien@gmail.com"

    def test_update_classroom(self, create_user):
        """ Test case to update a classroom.
         Args:  create_user (function): Fixture to create a user.   """
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
        """ Test case to delete a classroom.    """
        classroom = Classroom.safe_get(hash_key="test classroom")
        assert classroom
        classroom.delete()
        classroom = Classroom.safe_get(hash_key="test classroom")
        assert not classroom

class TestQuizTable: #Test cases for the Quiz table.
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
        """ Test case to create a new quiz.
        Args:
            create_quiz (function): Fixture to create a quiz.
            name (str): Name of the quiz.
            description (str): Description of the quiz.
            questions (list): List of questions.    """
        create_quiz(
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

        
    def test_read_quiz(self, created_quiz):
        """ Test case to read a quiz.
        Args:   create_quiz (function): Fixture to create a quiz.   """
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
        """ Test case to update a quiz.
        Args:
            create_quiz (function): Fixture to create a quiz.
            quiz_name (str): Name of the quiz to update.
            new_description (str): New description for the quiz.    """
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
        """ Test case to delete a quiz.
        Args:
            create_quiz (function): Fixture to create a quiz.
            quiz_name (str): Name of the quiz to delete.    """
        quiz = Quiz.safe_get(hash_key=quiz_name)
        assert quiz
        quiz.delete()
        deleted_quiz = Quiz.safe_get(hash_key=quiz_name)
        assert not deleted_quiz
        
