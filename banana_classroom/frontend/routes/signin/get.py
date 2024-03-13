from pypox.processing.base import processor
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.requests import Request


@processor()
async def endpoint(request: Request):
    if request.cookies.get("session") is not None:
        return RedirectResponse("/dashboard/activities/")
    if "user_type" not in request.query_params:
        return RedirectResponse("/signin?user_type=student")
    return request.state.template.TemplateResponse(request, "signin.html")
