from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.authentication import requires
from banana_classroom.database.NOSQL import banana_classroom
from starlette.exceptions import HTTPException


async def endpoint(request: Request):

    quiz_result = banana_classroom.QuizResult.safe_get(
        request.query_params.get("id", "")
    )

    if not quiz_result:
        raise HTTPException(detail="Quiz result not found", status_code=404)

    return request.state.template.TemplateResponse(
        request,
        "questions/results.html",
        context={"quiz_result": quiz_result},
    )
