from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from starlette import status
from banana_classroom.database.NOSQL.banana_classroom import User
from pypox.processing.base import processor
from pypox._types import BodyDict
from passlib.hash import bcrypt


@processor()
async def endpoint(body: BodyDict):
    user = User.safe_get(hash_key=body["email"])
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    if not bcrypt.verify(body["password"], user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    response = PlainTextResponse(
        "Login successful",
        status_code=200,
        headers={"hx-redirect": "/dashboard/activities/"},
    )
    response.set_cookie("authorization", user.email, httponly=True, samesite="strict")
    response.set_cookie("user_type", user.role, httponly=True, samesite="strict")
    return response
