from pypox.processing import processor, BodyDict
from starlette.responses import JSONResponse
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)
from starlette import status
from starlette.exceptions import HTTPException


@processor
async def endpoint(body: BodyDict):
    if not body.get("title", ""):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Title is required")
    if not type(body.get("title", "")) == str:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Title must be a string")
    if not body.get("description", ""):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Description is required")
    if not body.get("instructor", ""):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Instructor is required")
    if not type(body.get("instructor", "")) == str:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Instructor must be a string")
    classroom = Classroom(**body)
    classroom.save()
    return JSONResponse({"status": "success", "data": classroom.model_dump()})
