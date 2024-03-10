from pypox.processing.base import processor
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from banana_classroom.frontend.app import template


@processor()
async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return PlainTextResponse("Not authenticated", status_code=401)
    print("hello")
    return template.TemplateResponse(request, "dashboard/classroom.html")
