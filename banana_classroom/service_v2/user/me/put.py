from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette import status
from banana_classroom.database.NOSQL.banana_classroom import User
from pypox.processing.base import processor
from pypox._types import BodyDict, HeaderStr
from dyntastic import A
from datetime import datetime
from passlib.hash import bcrypt
from starlette.authentication import requires
from starlette.requests import Request


@requires(["authenticated"])
async def endpoint(request: Request):

    user = User.safe_get(hash_key=request.user.email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    body = await request.json()

    if "password" in body:
        user.update(A.password.set(bcrypt.hash(body.get("password", ""))))

    user.update(A.name.set(body.get("name", None or user.name)))
    user.update(A.updated_at.set(str(datetime.now())))
    return JSONResponse(
        user.model_dump(exclude={"password"}), status_code=status.HTTP_200_OK
    )
