from pypox.processing.base import processor
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from banana_classroom.frontend.app import template
from httpx import AsyncClient


@processor()
async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return PlainTextResponse("Not authenticated", status_code=401)

    async with AsyncClient(base_url="http://localhost:5000") as client:
        response = await client.get(
            "/api/v1/classroom/create/",
            headers={"Authorization": f"Basic {request.cookies.get('session')}"},
        )
        print(response.text)

    return template.TemplateResponse(request, "forms/classroom_create.html")
