from pypox.processing.base import processor
from pypox._types import QueryStr, BodyDict
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette import status
from starlette.authentication import requires
from datetime import datetime
from banana_classroom.database.NOSQL.banana_classroom import Quiz, Question, Classroom
from starlette.exceptions import HTTPException
from dyntastic import A


@requires(["authenticated", "instructor"])
async def endpoint(request: Request):

    classroom_id = request.query_params.get("class_id", "")

    classroom = Classroom.safe_get(hash_key=classroom_id)

    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found"
        )

    if classroom_id not in request.user.classrooms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Classroom not found"
        )

    body = await request.json()

    time = str(datetime.now())
    quiz = Quiz(**body, created_at=time, updated_at=time, classroom_id=classroom_id)
    quiz.save()

    quiz_questions = [
        (q.get("text", ""), q.get("option", []), q.get("answer", ""))
        for q in body["questions"]
    ]

    classroom.update(A.quizzes.append(quiz.id))
    request.user.update(A.quizzes.append(quiz.id))

    return JSONResponse(
        {"message": f"Quiz created successfully", "id": quiz.id},
        status_code=status.HTTP_201_CREATED,
    )
