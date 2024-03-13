from starlette.requests import Request
from starlette.authentication import requires
from banana_classroom.database.NOSQL.banana_classroom import Quiz, Classroom
from starlette.exceptions import HTTPException
from starlette import status

@requires(["authenticated", "student"])
async def endpoint(request: Request):
    quiz = Quiz.safe_get(hash_key=request.query_params["id"])
    if not quiz:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Quiz not found")
    classroom = Classroom.safe_get(hash_key=quiz.classroom_id)