from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from starlette import status
from banana_classroom.database.NOSQL.banana_classroom import User
from pypox.processing.base import processor
from pypox._types import HeaderStr
from starlette.authentication import requires
from starlette.requests import Request


@requires(["authenticated"])
async def endpoint(request: Request):
    user = User.safe_get(hash_key=request.user.email)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    user.delete()
    return PlainTextResponse(
        f"User {user.email} deleted", status_code=status.HTTP_204_NO_CONTENT
    )
