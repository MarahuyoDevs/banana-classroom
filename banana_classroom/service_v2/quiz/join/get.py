from starlette.requests import Request
from starlette.authentication import requires
from banana_classroom.database.NOSQL.banana_classroom import Quiz, Classroom


@requires(["authenticated", "student"])
async def endpoint(request: Request):
    quiz = Quiz.safe_get(hash_key=request.query_params["id"])
    if not quiz:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Quiz not found")
