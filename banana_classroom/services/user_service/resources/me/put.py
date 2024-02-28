from dyntastic import A
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.exceptions import HTTPException
from banana_classroom.services.user_service.databases.NOSQL.userNOSQL import (
    User,
)


async def endpoint(request: Request):

    user = User.safe_get(hash_key=request.headers.get("user-id", "1"))

    if not user:
        raise HTTPException(400, "User does not exists")
    body = await request.json()
    user.update(A.name.set(body.get("name", user.name)))
    user.update(A.email.set(body.get("email", user.email)))
    user.update(A.password.set(body.get("password", user.password)))
    user.save()
    return JSONResponse(user.model_dump(exclude={"password"}))
