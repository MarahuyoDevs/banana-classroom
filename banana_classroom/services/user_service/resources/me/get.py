from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.requests import Request
from banana_classroom.services.user_service.databases.NOSQL.userNOSQL import (
    User,
)


async def endpoint(request: Request):
    user = User.get(request.headers.get("user-id", "1"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(user.model_dump())
