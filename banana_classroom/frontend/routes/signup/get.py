from pypox.processing.base import processor
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.requests import Request
from httpx import AsyncClient, ASGITransport
from banana_classroom.service_v2.app import api_service
from starlette.testclient import TestClient


@processor()
async def endpoint(request: Request):
    if request.cookies.get("session") is not None:
        return RedirectResponse("/dashboard/activities/")
    return request.state.template.TemplateResponse(request, "signup.html")
