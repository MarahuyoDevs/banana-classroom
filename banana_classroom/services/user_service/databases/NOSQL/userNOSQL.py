from pydantic import BaseModel, Field, field_validator
from dyntastic import Dyntastic
from uuid import uuid4
from passlib.hash import pbkdf2_sha256
import os


class User(Dyntastic):

    __table_name__ = "user"
    __hash_key__ = "id"

    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    email: str
    password: str
    type: str = "user"  # admin, student, instructor

    @field_validator("name")
    def validate_name(cls, value) -> str:
        if not value:
            raise ValueError("Name cannot be empty")
        if "-" in value:
            raise ValueError("Name cannot contain hyphens")
        if "/" in value:
            raise ValueError("Name cannot contain slashes")
        return value

    @field_validator("email")
    def validate_email(cls, value) -> str:
        if not value:
            raise ValueError("Email cannot be empty")
        if "@" not in value:
            raise ValueError("@ is needed for email xd nyahaah")
        return value

    @field_validator("password")
    def validate_password(cls, value) -> str:
        if not value:
            raise ValueError("Password cannot be empty")
        if len(value) < 8:
            raise ValueError("Password must be atleast 8 characters long")
        return pbkdf2_sha256.hash(value)
