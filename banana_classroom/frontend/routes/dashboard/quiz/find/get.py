from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.authentication import requires


async def endpoint(request: Request):
    
    quiz = request.state.backend.get(f"/quiz/find/?id={request.query_params["id"]}",headers={
        "Authorization": f"Basic {request.cookies.get('session')}",
    })
        
    return request.state.template.TemplateResponse(request, "questions/identification.html", context={"quiz": quiz.json(),"len":len,"enumerate":enumerate})
