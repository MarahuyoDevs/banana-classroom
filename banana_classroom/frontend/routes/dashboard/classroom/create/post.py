from starlette.requests import Request
from starlette.responses import PlainTextResponse
from base64 import b64decode
from banana_classroom.database.NOSQL.banana_classroom import User, Classroom
from dyntastic import A
from starlette.exceptions import HTTPException
from starlette import status


async def endpoint(request: Request):

    body = await request.json()

    response = request.state.backend.post(
        "/classroom/create/",
        json=body,
        headers={"Authorization": f"Basic {request.cookies.get('session')}"},
    )
    return PlainTextResponse(
        "Classroom Created",
        status_code=201,
        headers={"hx-redirect": response.headers["hx-redirect"]},
    )
