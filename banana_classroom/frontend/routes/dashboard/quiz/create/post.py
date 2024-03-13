from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse
from banana_classroom.database.NOSQL.banana_classroom import Quiz
from starlette.exceptions import HTTPException


async def endpoint(request: Request):
    if request.cookies.get("session") is None:
        return RedirectResponse("/signin")

    response = request.state.backend.post(
        f"/quiz/create/?class_id={request.query_params['class_id']}",
        headers={
            "Authorization": f"Basic {request.cookies.get('session')}",
        },
        json=await request.json(),
    )

    if response.status_code != 201:
        raise HTTPException(
            detail="Failed to create quiz",
            status_code=400,
        )

    return PlainTextResponse(
        "/dashboard/classroom/",
        status_code=200,
        headers={"hx-redirect": f"/dashboard/quiz/find/?id={response.json()['id']}"},
    )
