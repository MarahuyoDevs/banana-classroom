from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.requests import Request
from banana_classroom.services.user_api.user_service.databases.NOSQL.userNOSQL import (
    User,
)
from pypox.processing import processor, QueryStr, BodyDict


async def endpoint(type: QueryStr, body: BodyDict):
    if User.safe_get(hash_key=body["email"]):
        raise HTTPException(400, "User already exists")
    user = User(**body, type=type)
    user.save()
    return JSONResponse({"message": "Sucessfully created user", "id": user.id})
