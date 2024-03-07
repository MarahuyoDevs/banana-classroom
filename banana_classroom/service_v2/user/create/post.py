from banana_classroom.database.NOSQL.banana_classroom import User
from pypox.processing.base import processor
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from starlette import status
from pypox._types import BodyDict, QueryStr
from dyntastic import A
from passlib.hash import bcrypt
from datetime import datetime


@processor()
async def endpoint(body: BodyDict, user_type: QueryStr):
    """Create a new user.

    This endpoint creates a new user with the provided information in the request body.

    Args:
        body (BodyDict): A dictionary containing the user information.

    Raises:
        HTTPException: If the user already exists.

    Returns:
        None
    """

    if body["password"] != body["confirm_password"]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Passwords do not match")
    if user_type not in ["student", "instructor"]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid user type")

    user = User(
        **body,
        role=user_type,
        created_at=str(datetime.now()),
        updated_at=str(datetime.now()),
    )

    # hash the password
    user.password = bcrypt.hash(user.password)

    if User.safe_get(user.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists")

    user.save()  # save the user to the database

    return PlainTextResponse(
        "User created successfully", status_code=201, headers={"hx-redirect": "/signin"}
    )
