from typing import Optional
from dyntastic import Dyntastic
from pydantic import BaseModel


class User(Dyntastic):

    id: str
    name: str
    email: str
    password: str  # hashed
    role: str  # student, teacher, admin
    created_at: str
    updated_at: str


class Classroom(Dyntastic):

    id: str
    name: str
    description: str
    instructor: str  # user_id
    students: list[str]  # user_id
    created_at: str
    updated_at: str


class Question(BaseModel):
    type: str
    text: str
    options: Optional[list[str]] = None
    answer: str


class Quiz(Dyntastic):

    id: str
    name: str
    description: str
    questions: list[Question]  # question_id
    created_at: str
    updated_at: str
