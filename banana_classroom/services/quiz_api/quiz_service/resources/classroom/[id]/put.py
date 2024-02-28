from pypox.processing import processor, BodyDict, PathStr
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)
from dyntastic import A


@processor
async def endpoint(id: PathStr, body: BodyDict):

    classroom = Classroom.safe_get(id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    classroom.update(A.title.set(body["title"]))
    classroom.update(A.description.set(body["description"]))
    classroom.update(A.instructor.set(body["instructor"]))

    return JSONResponse(classroom.model_dump())
