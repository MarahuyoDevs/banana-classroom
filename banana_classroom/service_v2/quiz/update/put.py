from pypox.processing.base import processor
from pypox._types import BodyDict, QueryStr
from banana_classroom.database.NOSQL.banana_classroom import Quiz, Question
from datetime import datetime
from starlette.responses import PlainTextResponse
from starlette import status
from starlette.exceptions import HTTPException
from dyntastic import A
from starlette.authentication import requires
from starlette.requests import Request


@processor()
async def endpoint(request: Request):

    quiz_id = request.query_params.get("quiz_id", "")
    body = await request.json()

    quiz = Quiz.safe_get(quiz_id)

    if not quiz:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Quiz not found")

    quiz.update(A.name.set(body.get("name", None) or quiz.name))
    quiz.update(A.description.set(body.get("description", None) or quiz.description))

    quiz.update(A.updated_at.set(str(datetime.now())))

    return PlainTextResponse(
        "Quiz updated successfully", status_code=status.HTTP_202_ACCEPTED
    )
