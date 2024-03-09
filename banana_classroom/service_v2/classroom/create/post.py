from banana_classroom.database.NOSQL.banana_classroom import Classroom
from pypox.processing.base import processor
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from starlette import status
from pypox._types import BodyDict, QueryStr
from dyntastic import A
from passlib.hash import bcrypt
from datetime import datetime
from pydantic import BaseModel

class ClassroomModel(BaseModel):
    name: str
    description: str
    instructor: str
@processor()
async def endpoint(body: BodyDict):
    time = str(datetime.now())
    request_body=ClassroomModel(**body)
    classroom = Classroom(
        name=request_body.name,
        description=request_body.description,
        instructor=request_body.instructor,
        created_at=time,
        updated_at=time,
    )

    classroom.save()

    return PlainTextResponse(
        "Classroom created successfully", status_code=201, headers={"hx-redirect": f"/dashboard/classroom/{classroom.id}"}
    )