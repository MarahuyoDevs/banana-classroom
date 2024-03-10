from starlette.responses import PlainTextResponse
from starlette.requests import Request
from httpx import AsyncClient


async def endpoint(request: Request):
    # login the user
    body = await request.json()
    main_response = PlainTextResponse(
        "Sucessfully logged in",
        status_code=200,
        headers={"hx-redirect": "/dashboard/activities/"},
    )
    async with AsyncClient(base_url="http://localhost:5000") as client:
        response = await client.post("/api/v1/security/token/", json=body)
        main_response.set_cookie(
            "session",
            response.json()["access_token"],
            httponly=True,
            max_age=60 * 60 * 24 * 7,
        )
        main_response.set_cookie(
            "role",
            response.json()["role"],
            httponly=True,
            max_age=60 * 60 * 24 * 7,
        )
    return main_response
