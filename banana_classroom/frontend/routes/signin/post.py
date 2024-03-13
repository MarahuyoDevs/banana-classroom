from starlette.responses import PlainTextResponse
from starlette.requests import Request
from httpx import AsyncClient
from starlette.exceptions import HTTPException


async def endpoint(request: Request):
    # login the user
    body = await request.json()
    user_type = request.query_params.get("user_type")
    main_response = PlainTextResponse(
        "Sucessfully logged in",
        status_code=200,
        headers={"hx-redirect": "/dashboard/activities/"},
    )
    response = request.state.backend.post(
        f"/security/token/?user_type={user_type}", json=body
    )
    if response.status_code != 200:
        raise HTTPException(
            detail="Invalid credentials",
            status_code=401,
        )
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
