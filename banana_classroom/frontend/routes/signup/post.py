from starlette.responses import PlainTextResponse
from starlette.requests import Request
from starlette.testclient import TestClient

async def endpoint(request: Request):
    # login the user
    body = await request.json()

    print(body)

    client: TestClient = request.state.backend
    
    client.post(f"/user/create/?user_type={request.query_params.get("user_type", "")}", json=body)

    return PlainTextResponse(
        "Sucessfully logged in",
        status_code=200,
        headers={"hx-redirect": "/signin/"},
    )
