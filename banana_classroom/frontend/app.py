import os
from pypox.application import Pypox
from pypox.router import HTTPRouter
from starlette.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from contextlib import asynccontextmanager
from typing import Any, TypedDict, AsyncIterator
from starlette.testclient import TestClient
from banana_classroom.service_v2.app import api_service
from banana_classroom.database.NOSQL import banana_classroom
from starlette.applications import Starlette
from dotenv import load_dotenv

import boto3

load_dotenv(override=True)


class State(TypedDict):
    template: Jinja2Templates
    backend: TestClient
    dynamodb: Any


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[State]:

    templates = Jinja2Templates(os.path.dirname(__file__) + "/templates/")

    if os.getenv("MODE", "") == "development":
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=os.environ["DYNTASTIC_REGION"],
            endpoint_url=os.environ["DYNTASTIC_HOST"],
        )
    else:
        dynamodb = boto3.resource("dynamodb")

    if "users" not in dynamodb.meta.client.list_tables()["TableNames"]:
        banana_classroom.User.create_table()

    if "classrooms" not in dynamodb.meta.client.list_tables()["TableNames"]:
        banana_classroom.Classroom.create_table()

    if "quizzes" not in dynamodb.meta.client.list_tables()["TableNames"]:
        banana_classroom.Quiz.create_table()

    if "quizzesresult" not in dynamodb.meta.client.list_tables()["TableNames"]:
        banana_classroom.QuizResult.create_table()

    try:
        with TestClient(api_service) as client:
            yield {"template": templates, "backend": client, "dynamodb": dynamodb}
    finally:
        pass


frontend_app = Pypox(
    [HTTPRouter(os.path.dirname(__file__) + "/routes")], lifespan=lifespan
)
