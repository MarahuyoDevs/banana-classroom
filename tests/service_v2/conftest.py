from typing import Callable
import pytest
from starlette.testclient import TestClient
from faker import Faker
from datetime import datetime
import boto3
from banana_classroom.database.NOSQL.banana_classroom import (
    User,
    Classroom,
    Quiz,
    Question,
)
import random
import os
from banana_classroom.service_v2.app import api_service
from banana_classroom.frontend.app import frontend_app


@pytest.fixture
def service_v2_client() -> TestClient:
    return TestClient(api_service)


@pytest.fixture
def service_v2_frontend() -> TestClient:  # type: ignore
    with TestClient(frontend_app) as client:
        yield client  # type: ignore


@pytest.fixture()
def service_v2_authenticated_client(service_v2_client) -> Callable[[User], TestClient]:

    def decorator(user: User) -> TestClient:
        client = service_v2_client
        # login the user
        response = client.post(
            f"/security/token/?user_type={user.role}",
            json={"email": user.email, "password": user.password},
        )
        assert response.status_code == 200
        client.headers.update(
            {"Authorization": f"Basic {response.json()['access_token']}"}
        )

        return client

    return decorator


@pytest.fixture
def create_user():
    """Fixture to create a user in the database.
    Returns a function that takes name, email, password, role, created_at, and updated_at as arguments and returns a User object.
    """

    def create(role: str):
        fake = Faker()
        created_at = str(datetime.now())
        updated_at = str(datetime.now())
        user = User(
            name=fake.name(),
            email=fake.email(),
            password="mypassword",
            role=role,
            created_at=created_at,
            updated_at=updated_at,
        )
        return user, created_at, updated_at

    return create


@pytest.fixture
def create_quiz(
    create_question: Callable[[str], tuple[Question, str, str]]
) -> Callable[[str], tuple[Quiz, str, str]]:
    """Fixture to create a quiz in the database.
    Returns a function that takes name, description, questions, created_at, and updated_at as arguments and returns a Quiz object.
    """

    def _create(
        classroom_id: str,
    ) -> tuple[Quiz, str, str]:
        fake = Faker()
        created_at = str(datetime.now())
        updated_at = str(datetime.now())

        quiz = Quiz(
            name=fake.name(),
            classroom_id=classroom_id,
            description=fake.paragraph(),
            created_at=created_at,
            updated_at=updated_at,
        )

        quiz.questions = [create_question(quiz.id)[0] for _ in range(5)]

        return quiz, created_at, updated_at

    return _create


@pytest.fixture
def create_question():
    """Fixture to create a question in the database.
    Returns a function that takes quiz_id, type, text, options, answer, created_at, and updated_at as arguments and returns a Question object.
    """

    def _create(
        quiz_id: str,
    ):
        fake = Faker()
        created_at = str(datetime.now())
        updated_at = str(datetime.now())
        question = Question(
            quiz_id=quiz_id,
            type=random.choice(["multiple_choice", "true_false"]),
            text=fake.paragraph(),
            answer=fake.text(),
            index=random.randint(0, 10),
            created_at=created_at,
            updated_at=updated_at,
        )
        return question, created_at, updated_at

    return _create


@pytest.fixture()
def create_classroom():
    """Fixture to create a classroom in the database.
    Returns a function that takes name, description, instructor, students, quizzes, created_at, and updated_at as arguments and returns a Classroom object.
    """

    def _create(
        name: str, description: str, instructor: User
    ) -> tuple[Classroom, str, str]:

        created_at = str(datetime.now())
        updated_at = str(datetime.now())
        classroom = Classroom(
            name=name,
            description=description,
            instructor=instructor.email,
            students=[],
            created_at=created_at,
            updated_at=updated_at,
        )
        return classroom, created_at, updated_at

    return _create


@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
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

    if "quizzes" not in dynamodb.meta.client.list_tables()["TableNames"]:
        Quiz.create_table()


@pytest.fixture
def create_authenticated_user(
    service_v2_client: TestClient,
    create_user: Callable[[str], tuple[User, str, str]],
):
    """Fixture to create an authenticated user in the database.
    Returns a function that takes name, email, password, role, created_at, and updated_at as arguments and returns a User object.
    """

    def create(role: str) -> User:
        user = create_user(role)[0]
        response = service_v2_client.post(
            f"/user/create/?user_type={user.role}",
            json={
                **user.model_dump(exclude={"created_at", "updated_at"}),
                "confirm_password": user.password,
            },
        )
        assert response.status_code == 201
        return user

    return create
