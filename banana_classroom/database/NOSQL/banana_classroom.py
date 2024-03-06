from typing import Optional
from uuid import uuid4
from dyntastic import Dyntastic
from pydantic import BaseModel, Field


class User(Dyntastic):

    __table_name__ = "users"
    __hash_key__ = "email"

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    email: str
    password: str  # hashed
    role: str  # student, teacher, admin
    created_at: str
    updated_at: str


class Classroom(Dyntastic):

    __table_name__ = "classrooms"
    __hash_key__ = "name"

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    instructor: str  # user_id
    students: list[str]  # user_id
    created_at: str
    updated_at: str


class Question(BaseModel):

    id: str = Field(default_factory=lambda: str(uuid4()))
    type: str
    text: str
    options: Optional[list[str]] = None
    answer: str


class Quiz(Dyntastic):

    __table_name__ = "quiz"
    __hash_key__ = "id"

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: str
    questions: list[Question]  # question_id
    created_at: str
    updated_at: str
