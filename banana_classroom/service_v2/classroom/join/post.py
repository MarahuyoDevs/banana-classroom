from banana_classroom.database.NOSQL.banana_classroom import Classroom, User
from starlette.responses import PlainTextResponse
from dyntastic import A
from datetime import datetime
from pydantic import BaseModel
from starlette.authentication import requires
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette import status


@requires(["authenticated"])
async def endpoint(request: Request):

    classroom_id = request.query_params.get("class_id", "")
    classroom = Classroom.safe_get(hash_key=classroom_id)

    if not classroom:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Classroom not found")

    if request.user.id in classroom.students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already joined classroom",
            headers={"hx-redirect": f"/dashboard/classroom/{classroom.id}"},
        )

    classroom.update(A.students.append(request.user.email))
    request.user.update(A.classrooms.append(classroom.id))

    return PlainTextResponse(
        "Successfully joined classroom",
        status_code=201,
        headers={"hx-redirect": f"/dashboard/classroom/{classroom.id}"},
    )
