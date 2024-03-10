from starlette.requests import Request
from starlette.responses import PlainTextResponse


async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return PlainTextResponse("Not authenticated", status_code=401)

    response = PlainTextResponse(
        "Successfully signed out", status_code=303, headers={"hx-redirect": "/signin"}
    )
    response.delete_cookie("session")
    response.delete_cookie("role")
    return response
