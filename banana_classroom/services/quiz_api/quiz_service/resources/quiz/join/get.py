from pypox.processing import processor, QueryStr
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)


@processor
async def endpoint(class_id: QueryStr, quiz_id: QueryStr):

    classroom = Classroom.safe_get(class_id)

    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    if not classroom.quizzes:
        raise HTTPException(status_code=404, detail="No quizzes found")

    for quiz in classroom.quizzes:
        if quiz.id == quiz_id:
            return JSONResponse([x.model_dump() for x in quiz.questions])

    return JSONResponse(classroom.model_dump())
