from pypox.processing.base import processor
from pypox._types import BodyDict
from starlette.responses import JSONResponse
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)
from starlette import status
from starlette.exceptions import HTTPException


@processor()
async def endpoint(body: BodyDict):

    title = body.get("title", "")
    if not title:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Title is required"
        )
    if not isinstance(title, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title must be a string",
        )
    if len(title) > 60:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="ensure this value has at most 60 characters",
        )

    description = body.get("description", "")
    if not description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Description is required",
        )
    if len(description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="ensure this value has at most 1000 characters",
        )

    instructor = body.get("instructor", "")
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Instructor is required",
        )
    if not isinstance(instructor, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Instructor must be a string",
        )
    if len(instructor) > 30:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="ensure this value has at most 30 characters",
        )

    classroom = Classroom(**body)
    classroom.save()
    return JSONResponse({"status": "success", "data": classroom.model_dump()})
