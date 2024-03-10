from starlette.requests import Request
from starlette.responses import PlainTextResponse
from base64 import b64decode
from banana_classroom.database.NOSQL.banana_classroom import User, Classroom
from datetime import datetime
from dyntastic import A
from starlette.exceptions import HTTPException
from starlette import status


async def endpoint(request: Request):

    body = await request.json()
    email, password = b64decode(request.cookies.get("session", "")).decode().split(":")

    user = User.safe_get(email)
    if not user:
        raise HTTPException(detail="User not found", status_code=404)

    if user.role != "instructor":
        raise HTTPException(
            detail="Must be instructor", status_code=status.HTTP_401_UNAUTHORIZED
        )
        
    time = str(datetime.now())
    classroom = Classroom(
        name=body["name"],
        description=body["description"],
        instructor=user.email,
        created_at=time,
        updated_at=time,
    )
    classroom.save()
    user.update(A.classrooms.append(classroom.id))
    return PlainTextResponse(
        "Classroom Created",
        status_code=201,
        headers={"hx-redirect": f"/dashboard/classroom/find/?id={classroom.id}"},
    )
