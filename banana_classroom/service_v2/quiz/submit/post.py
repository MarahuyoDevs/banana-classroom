from pypox.processing.base import processor
from pypox._types import BodyDict, QueryStr
from banana_classroom.database.NOSQL import banana_classroom
from datetime import datetime
from starlette.responses import PlainTextResponse, JSONResponse
from starlette import status
from dyntastic import A
from pydantic import BaseModel
from starlette.authentication import requires
from starlette.requests import Request


@requires(["authenticated"])
async def endpoint(request: Request):

    quiz_id = request.query_params.get("id", "")

    body = await request.json()
    quiz_result = banana_classroom.QuizResult(
        quiz_id=quiz_id,
        user_email=request.user.email,
        answers=body["answers"],
        score=body["score"],
    )
    quiz_result.save()

    request.user.update(A.quizzes_result.append(quiz_result.id))
    return JSONResponse(
        {"message": "Successfully submitted", "id": quiz_result.id},
        status_code=status.HTTP_201_CREATED,
    )
