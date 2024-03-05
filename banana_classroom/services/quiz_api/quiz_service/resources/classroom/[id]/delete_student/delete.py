from pypox.processing import PathStr, BodyDict, processor
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import Classroom
from starlette.exceptions import HTTPException
from starlette import status
from starlette.responses import JSONResponse

@processor
async def endpoint(id: PathStr, body: BodyDict):
    # Check if the classroom exists
    classroom = Classroom.safe_get(id)
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classroom not found",
        )

    # Check if student_id is provided and is a string
    student_id = body.get("student_id")
    if not student_id or not isinstance(id, str):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid or missing student ID",
        )

    # Check if the student is in the classroom
    if student_id not in classroom.students:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Student is not in the classroom",
        )

    # Remove the student from the classroom and save the changes
    classroom.students.remove(id)
    classroom.save()

    return JSONResponse({"status": "success", "data": classroom.model_dump()})
