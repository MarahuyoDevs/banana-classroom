from pypox.processing.base import processor
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from banana_classroom.frontend.app import template


@processor()
async def page(request: Request):
    return template.TemplateResponse(request, "dashboard/forms/classroom_create.html")
