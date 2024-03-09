from pypox.processing.base import processor
from pypox._types import QueryStr,BodyDict
from starlette.responses import PlainTextResponse,JSONResponse
from starlette import status
from datetime import datetime
from dyntastic import A
from banana_classroom.database.NOSQL.banana_classroom import Quiz,Question

@processor()
async def endpoint(quiz_id: QueryStr):
    quiz = Quiz.safe_get(quiz_id)
    if not quiz:
        return PlainTextResponse("Quiz not found", status_code=status.HTTP_404_NOT_FOUND)
    
    quiz.questions = [Question.safe_get(q) for q in quiz.questions]
    return JSONResponse(quiz.model_dump())