from pypox.processing.base import processor
from starlette.responses import PlainTextResponse
from starlette.requests import Request


@processor()
async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return PlainTextResponse("Not authenticated", status_code=401)
    # get the user info
    # get the classroom info
    user = request.state.backend.get(
        "/user/me/",
        headers={"Authorization": f"Basic {request.cookies.get('session')}"},
    ).json()
    classrooms = []
    for classroom in user["classrooms"]:
        room = request.state.backend.get(
            f"/classroom/find/?id={classroom}",
            headers={"Authorization": f"Basic {request.cookies.get('session')}"},
        )
        classrooms.append(room.json())

    return request.state.template.TemplateResponse(
        request,
        "dashboard/classroom.html",
        context={"classrooms": classrooms, "user": user},
    )
