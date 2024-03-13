from starlette.requests import Request
from starlette.responses import PlainTextResponse
from base64 import b64decode
from banana_classroom.database.NOSQL.banana_classroom import User, Classroom
from starlette.exceptions import HTTPException
from starlette import status


async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return PlainTextResponse("Not authenticated", status_code=401)
    return request.state.template.TemplateResponse(
        request, "forms/classroom_invite.html"
    )
