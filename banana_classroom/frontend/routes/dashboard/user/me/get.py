from pypox.processing.base import processor
from starlette.responses import PlainTextResponse
from starlette.requests import Request


@processor()
async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return PlainTextResponse("Not authenticated", status_code=401)
    return request.state.template.TemplateResponse(request, "dashboard/profile.html")
