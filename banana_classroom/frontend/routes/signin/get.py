from pypox.processing.base import processor
from starlette.responses import PlainTextResponse, RedirectResponse

from starlette.requests import Request
from banana_classroom.frontend.app import template


@processor()
async def endpoint(request: Request):
    if request.cookies.get("session") is not None:
        return RedirectResponse("/dashboard/activities/")
    if "user_type" not in request.query_params:
        return RedirectResponse("/signin?user_type=student")
    return template.TemplateResponse(request, "signin.html")
