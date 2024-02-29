from datetime import datetime 
from typing import Optional
from dyntastic import Dyntastic
from pydantic import BaseModel, Field
from uuid import uuid4


class Classroom(Dyntastic):

    __hash_key__ = "id"
    __table_name__ = "classroom"

    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    instructor: str
    students: Optional[list[str]] = None
    quizzes: Optional[list["Quiz"]] = None


class Student(BaseModel):
    id: str
    name: str
    completed_quizzes: list[str]
    incompleted_quizzes: list[str]


class QuizResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    score: int
    title: str
    description: str
    instructor: str
    questions: Optional[list[tuple[str, bool]]] = None


class Quiz(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    instructor: str
    questions: list["Question"]
    show_result: bool = False
    expiration_time: datetime #expiration of quiz availability


class Question(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    description: str
    options: Optional[list[str]] = None  # optional choice
    answer: str
