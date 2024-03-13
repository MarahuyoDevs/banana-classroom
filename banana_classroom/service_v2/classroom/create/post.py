from banana_classroom.database.NOSQL.banana_classroom import Classroom, User
from pypox.processing.base import processor
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from starlette import status
from pypox._types import BodyDict, QueryStr
from dyntastic import A
from passlib.hash import bcrypt
from datetime import datetime
from pydantic import BaseModel
from starlette.authentication import requires
from starlette.requests import Request


class ClassroomModel(BaseModel):
    name: str
    description: str


@requires(["authenticated", "instructor"])
async def endpoint(request: Request):

    time = str(datetime.now())
    request_body = ClassroomModel(**await request.json())
    classroom = Classroom(
        name=request_body.name,
        description=request_body.description,
        instructor=request.user.email,
        created_at=time,
        updated_at=time,
    )

    request.user.update(A.classrooms.append(classroom.id))
    classroom.save()

    return PlainTextResponse(
        "Classroom created successfully",
        status_code=201,
        headers={"hx-redirect": f"/dashboard/classroom/find/?id={classroom.id}"},
    )
