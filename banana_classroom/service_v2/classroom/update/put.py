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

class UpdateClassroomModel(BaseModel):
    description: str
    instructor: str
@processor()
async def endpoint(body: BodyDict, classroom_name:QueryStr):
    classroom = Classroom.safe_get(hash_key=classroom_name)
    if not classroom:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Classroom not found")
    request_body=UpdateClassroomModel(**body)
    classroom.update(A.description.set(request_body.description or classroom.instructor))
    classroom.update(A.instructor.set(request_body.instructor or classroom.instructor))
    classroom.update(A.updated_at.set(str(datetime.now())))

    return PlainTextResponse(
        "Classroom updated successfully", status_code=status.HTTP_202_ACCEPTED, headers={"hx-redirect": f"/dashboard/classroom/{classroom.id}"}
    )
