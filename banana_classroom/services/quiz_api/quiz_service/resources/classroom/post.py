from pypox.processing import processor, BodyDict
from starlette.responses import JSONResponse
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)


@processor
async def endpoint(body: BodyDict):
    classroom = Classroom(**body)
    classroom.save()
    return JSONResponse({"status": "success", "data": classroom.model_dump()})
