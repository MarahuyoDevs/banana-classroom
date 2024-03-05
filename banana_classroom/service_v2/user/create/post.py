from banana_classroom.database.NOSQL.banana_classroom import User
from pypox.processing.base import processor
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette import status
from pypox._types import BodyDict
from dyntastic import A
from passlib.hash import bcrypt


@processor()
async def endpoint(body: BodyDict):
    """Create a new user.

    This endpoint creates a new user with the provided information in the request body.

    Args:
        body (BodyDict): A dictionary containing the user information.

    Raises:
        HTTPException: If the user already exists.

    Returns:
        None
    """

    user = User(**body)

    # hash the password
    user.password = bcrypt.hash(user.password)

    if User.query(A.email == user.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists")

    user.save()  # save the user to the database

    return JSONResponse(user.model_dump(exclude={"password"}))
