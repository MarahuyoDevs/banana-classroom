import os
from starlette.testclient import TestClient
from banana_classroom.database.NOSQL.banana_classroom import User, Classroom
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
        users = [x for x in User.scan((A.role == "student"))]  # type: ignore
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

        # aight aight wla tulog e
