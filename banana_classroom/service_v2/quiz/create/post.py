from pypox.processing.base import processor
from pypox._types import QueryStr,BodyDict
from starlette.responses import PlainTextResponse
from starlette import status
from datetime import datetime
from banana_classroom.database.NOSQL.banana_classroom import Quiz,Question

@processor()
async def endpoint(body:BodyDict):
    time = str(datetime.now())
    quiz = Quiz(**body,created_at=time,updated_at=time)
    quiz.save()
    questions = [Question(**q,created_at=time,updated_at=time,quiz_id=quiz.id) for q in body['questions']] 
    map(lambda q: q.save(), questions) 
    return PlainTextResponse(f"Quiz created successfully", status_code=status.HTTP_201_CREATED)