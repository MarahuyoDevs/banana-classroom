from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.exceptions import HTTPException
from banana_classroom.services.user_service.databases.NOSQL.userNOSQL import (
    User,
)


async def endpoint(request: Request):
    user = User.get(request.headers.get("user-id", "1"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return JSONResponse({"message": f"User {user.id} deleted"})
