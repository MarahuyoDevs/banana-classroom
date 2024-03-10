from pypox.processing.base import processor
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from banana_classroom.frontend.app import template
from banana_classroom.database.NOSQL.banana_classroom import Classroom
from starlette.exceptions import HTTPException
from starlette import status


@processor()
async def endpoint(request: Request):

    class_id = request.query_params.get("id", "")

    if request.cookies.get("session") is None:
        return PlainTextResponse("Not authenticated", status_code=401)

    classroom = Classroom.safe_get(class_id)

    if not classroom:
        raise HTTPException(
            detail="Classroom does not exist", status_code=status.HTTP_404_NOT_FOUND
        )

    print(classroom)

    return template.TemplateResponse(
        request, "dashboard/classroom.html", context={"classroom": classroom}
    )
