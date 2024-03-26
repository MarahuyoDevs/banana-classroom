from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse, JSONResponse
from starlette import status
from banana_classroom.database.NOSQL.banana_classroom import User
from pypox.processing.base import processor
from pypox._types import BodyDict
from passlib.hash import bcrypt
from base64 import b64encode
from starlette.requests import Request


@processor()
async def endpoint(request: Request):
    body = await request.json()
    user = User.safe_get(hash_key=body["input-email"])
    user_type = request.query_params.get("user_type")
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    if not bcrypt.verify(body["input-password"], user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    if user.role != user_type:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid role")
    return JSONResponse(
        {
            "access_token": b64encode(
                f"{user.email}:{user.password}".encode()
            ).decode(),
            "token_type": "basic",
            "role": user.role,
        },
        status_code=200,
    )
