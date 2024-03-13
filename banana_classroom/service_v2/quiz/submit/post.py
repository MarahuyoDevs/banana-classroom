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

    body = await request.json()

    quiz_result = banana_classroom.QuizResult(
        quiz_id=body["quiz"]["id"],
        user_id=body["user"]["id"],
        answers=body["answers"],
        score=sum([x[-1] for x in body["answers"].values() if x[-1] is True]),
    )
    quiz_result.save()

    request.user.update(A.quizzes_result.append(quiz_result.id))

    return JSONResponse(
        {"message": "Successfully submitted", "id": quiz_result.id},
        status_code=status.HTTP_201_CREATED,
    )
