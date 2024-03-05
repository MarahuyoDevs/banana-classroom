from pypox.processing.base import processor
from pypox._types import PathStr
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)


@processor()
async def endpoint(id: PathStr):
    classroom = Classroom.safe_get(id)

    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    return JSONResponse(classroom.model_dump())
