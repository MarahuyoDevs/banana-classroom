from pypox.processing.base import processor
from pypox._types import BodyDict
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from dyntastic import A
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
    Question,
    Quiz,
)


@processor()
async def endpoint(body: BodyDict):
    classroom = Classroom.safe_get(body.get("class_id", ""))

    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    quiz = Quiz(**body)

    if not classroom.quizzes:
        classroom.update(A.quizzes.set([quiz.model_dump()]))

    classroom.update(A.quizzes.append(quiz.model_dump()))

    return JSONResponse({"status": "success", "data": quiz.model_dump()})
