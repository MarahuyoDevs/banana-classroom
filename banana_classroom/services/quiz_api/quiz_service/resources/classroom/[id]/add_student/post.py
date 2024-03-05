from pypox.processing import PathStr, BodyDict, processor
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
)
from starlette.exceptions import HTTPException
from starlette import status
from starlette.responses import JSONResponse
from dyntastic import A


@processor
async def endpoint(id: PathStr, body: BodyDict):

    if not Classroom.safe_get(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found",
        )

    if not body.get("student_id", ""):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Student ID is required",
        )

    if not isinstance(body.get("student_id", ""), str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Student ID must be a string",
        )

    classroom = Classroom.safe_get(id)
    # Check if student ID is provided and is a string
    student_id = body.get("student_id")
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Student ID is required",
        )
    if not isinstance(student_id, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Student ID must be a string",
        )

    # Check if student already exists in the classroom
    if student_id in classroom.students:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Student already exists in the classroom",
        )

    # Add student to the classroom and return the updated classroom data
    classroom.students.append(student_id)
    classroom.save()

    return JSONResponse({"status": "success", "data": classroom.model_dump()})
