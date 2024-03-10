from starlette.responses import RedirectResponse
from starlette.requests import Request


async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return RedirectResponse("/signin")
    else:
        return RedirectResponse("/dashboard/activities")
