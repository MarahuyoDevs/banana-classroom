from pypox.processing.base import processor
from starlette.responses import PlainTextResponse
from starlette.requests import Request


@processor()
async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return PlainTextResponse("Not authenticated", status_code=401)
    user = request.state.backend.get(
        "/user/me/",
        headers={"Authorization": f"Basic {request.cookies.get('session')}"},
    ).json()

    classroom = []
    quizzes = []

    for my_class in user["classrooms"]:
        room = request.state.backend.get(
            f"/classroom/find/?id={my_class}",
            headers={"Authorization": f"Basic {request.cookies.get('session')}"},
        )
        assert room.status_code != 404
        classroom.append(room.json())

    for my_quiz in user["quizzes"]:
        quiz = request.state.backend.get(
            f"/quiz/find/?id={my_quiz}",
            headers={"Authorization": f"Basic {request.cookies.get('session')}"},
        )
        assert quiz.status_code != 404
        quizzes.append(quiz.json())

    return request.state.template.TemplateResponse(
        request,
        "dashboard/activities.html",
        context={"classrooms": classroom, "quizzes": quizzes, "user": user},
    )
