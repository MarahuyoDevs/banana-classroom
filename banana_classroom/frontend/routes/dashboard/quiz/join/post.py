from banana_classroom.database.NOSQL.banana_classroom import Classroom, User
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.exceptions import HTTPException
from base64 import b64decode
from dyntastic import A


async def endpoint(request: Request):

    body = await request.json()

    return PlainTextResponse(
        "Joined Quiz",
        status_code=201,
        headers={"hx-redirect": f"/dashboard/quiz/find/?id={body.get('quiz_id')}"},
    )
