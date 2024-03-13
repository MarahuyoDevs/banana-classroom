from pypox.processing.base import processor
from pypox._types import QueryStr, BodyDict
from starlette.responses import PlainTextResponse, JSONResponse
from starlette import status
from datetime import datetime
from dyntastic import A
from banana_classroom.database.NOSQL.banana_classroom import Quiz, Question
from starlette.authentication import requires
from starlette.requests import Request


@requires(["authenticated"])
async def endpoint(request: Request):
    quiz = Quiz.safe_get(request.query_params.get("id", ""))
    if not quiz:
        return PlainTextResponse(
            "Quiz not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(quiz.model_dump())
