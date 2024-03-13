from banana_classroom.database.NOSQL.banana_classroom import Classroom, User
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.exceptions import HTTPException
from base64 import b64decode
from dyntastic import A


async def endpoint(request: Request):

    body = await request.json()

    response = request.state.backend.post(
        f"/classroom/join/?class_id={body.get('class_id')}",
        headers={"Authorization": f"Basic {request.cookies.get('session')}"},
    )

    print(response.text)

    return PlainTextResponse(
        "Joined Classroom",
        status_code=201,
        headers={
            "hx-redirect": f"/dashboard/classroom/find/?id={body.get('class_id')}"
        },
    )
