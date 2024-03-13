"""from contextlib import asynccontextmanager
from mangum import Mangum
from starlette.applications import Starlette
from banana_classroom.service_v2.app import api_service
from banana_classroom.frontend.app import frontend_app
from banana_classroom.database.NOSQL.banana_classroom import (
    User,
    Classroom,
    Quiz,
    Question,
)
from dotenv import load_dotenv
import boto3
import os
from typing import Any, TypedDict, AsyncIterator

load_dotenv()


class State(TypedDict):
    dynamodb: Any


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[State]:

    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.environ["DYNTASTIC_REGION"],
        endpoint_url=os.environ["DYNTASTIC_HOST"],
    )

    if "users" not in dynamodb.meta.client.list_tables()["TableNames"]:
        User.create_table()

    if "classrooms" not in dynamodb.meta.client.list_tables()["TableNames"]:
        Classroom.create_table()

    if "quizzes" not in dynamodb.meta.client.list_tables()["TableNames"]:
        Quiz.create_table()

    yield {"dynamodb": dynamodb}


app = Starlette()

app.mount("/api/v1/", api_service, name="api")
app.mount("/", frontend_app, name="frontend")

handler = Mangum(app)
"""
