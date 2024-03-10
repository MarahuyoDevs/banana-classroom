from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse
from banana_classroom.database.NOSQL.banana_classroom import Quiz
from httpx import AsyncClient


async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return RedirectResponse("/signin")
    body = Quiz(
        classroom_id=request.query_params.get("classroom_id", ""),
        **await request.json(),
        created_at="",
        updated_at="",
    )
    async with AsyncClient(base_url="http://localhost:5000") as client:
        response = await client.post(
            f"/api/v1/quiz/create/?classroom_id={body.classroom_id}",
            json=body.model_dump(exclude={"created_at", "updated_at"}),
        )
        print(response.text)
    return PlainTextResponse(
        "/dashboard/activities/",
        status_code=200,
        headers={"hx-redirect": "/dashboard/activities/"},
    )
