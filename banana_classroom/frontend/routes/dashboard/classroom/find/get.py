from pypox.processing.base import processor
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from banana_classroom.database.NOSQL.banana_classroom import Classroom
from starlette.exceptions import HTTPException
from starlette import status


@processor()
async def endpoint(request: Request):

    class_id = request.query_params.get("id", "")
    classroom = request.state.backend.get(
        f"/classroom/find/?id={class_id}",
        headers={"Authorization": f"Basic {request.cookies.get('session')}"},
    )

    if classroom.status_code == 404:
        raise HTTPException(
            detail="Classroom does not exist", status_code=status.HTTP_404_NOT_FOUND
        )

    classroom_body = classroom.json()

    if classroom.status_code == 404:
        raise HTTPException(
            detail="Classroom does not exist", status_code=status.HTTP_404_NOT_FOUND
        )

    students = []
    quizzes = []

    for student in classroom_body["students"]:
        response = request.state.backend.get(
            f"/user/find/?email={student}",
            headers={"Authorization": f"Basic {request.cookies.get('session')}"},
        )
        if response.status_code == 404:
            continue
        students.append(response.json())

    for quiz in classroom_body["quizzes"]:
        response = request.state.backend.get(
            f"/quiz/find/?id={quiz}",
            headers={"Authorization": f"Basic {request.cookies.get('session')}"},
        )
        if response.status_code == 404:
            continue
        quizzes.append(response.json())

    return request.state.template.TemplateResponse(
        request,
        "dashboard/classroom.html",
        context={
            "classroom": classroom_body,
            "students": students,
            "quizzes": quizzes,
        },
    )
