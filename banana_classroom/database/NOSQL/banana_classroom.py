from typing import Optional
from uuid import uuid4
from dyntastic import Dyntastic
from pydantic import BaseModel, Field
from datetime import datetime


class User(Dyntastic):

    __table_name__ = "users"
    __hash_key__ = "email"

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(validation_alias="input-name")
    email: str = Field(validation_alias="input-email")
    password: str = Field(validation_alias="input-password")
    role: str  # student, teacher, admin
    classrooms: list[str] = []  # classroom_id
    quizzes: list[str] = []  # quiz_id
    quizzes_result: list[str] = []  # quiz_result_id
    created_at: str
    updated_at: str


class Classroom(Dyntastic):

    __table_name__ = "classrooms"
    __hash_key__ = "id"

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    instructor: str  # user_id
    students: list[str] = []  # user_id
    quizzes: list[str] = []  # quiz_id
    created_at: str
    updated_at: str


class Question(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))
    quiz_id: str
    type: str 
    text: str
    index: int
    options: list[str] = []
    answer: str
    created_at: str
    updated_at: str


class Quiz(Dyntastic):

    __table_name__ = "quizzes"
    __hash_key__ = "id"

    id: str = Field(default_factory=lambda: str(uuid4()))
    classroom_id: str
    name: str
    description: str
    questions: list[Question] = []  # question obj
    created_at: str = Field(default_factory=lambda: str(datetime.now()))
    updated_at: str = Field(default_factory=lambda: str(datetime.now()))


class QuizResult(Dyntastic):
    __table_name__ = "quizzesresult"
    __hash_key__ = "id"
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    quiz_id: str
    score: int
    answers: dict[str, tuple[str, str, str, bool]]
    created_at: str = Field(default_factory=lambda: str(datetime.now()))
    updated_at: str = Field(default_factory=lambda: str(datetime.now()))
