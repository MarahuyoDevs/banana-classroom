from banana_classroom.database.NOSQL.banana_classroom import Classroom, User
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.exceptions import HTTPException
from base64 import b64decode
from dyntastic import A


async def endpoint(request: Request):

    body = await request.json()

    classroom = Classroom.safe_get(hash_key=body.get("class_id"))

    if not classroom:
        raise HTTPException(detail="Classroom not found", status_code=404)

    email, password = b64decode(request.cookies.get("session", "")).decode().split(":")

    user = User.safe_get(email)

    if not user:
        raise HTTPException(detail="Not user", status_code=404)

    if user.role != "student":
        raise HTTPException(detail="Must be student only", status_code=401)

    classroom.update(A.students.append(user.email))

    return PlainTextResponse(
        "Joined Classroom",
        status_code=201,
        headers={"hx-redirect": f"/dashboard/classroom/find/?id={classroom.id}"},
    )
