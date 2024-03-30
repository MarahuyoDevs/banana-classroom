from starlette.authentication import requires
from starlette.requests import Request
from banana_classroom.database.NOSQL import banana_classroom
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse


@requires(["authenticated"])
async def endpoint(request: Request):

    # quiz_result id
    quiz_result_id = request.query_params.get("id")

    if not quiz_result_id:
        raise HTTPException(status_code=400, detail="Missing quiz result id")

    quiz_result = banana_classroom.QuizResult.safe_get(hash_key=quiz_result_id)

    if not quiz_result:
        raise HTTPException(status_code=404, detail="Quiz result not found")

    return JSONResponse(quiz_result.model_dump())
