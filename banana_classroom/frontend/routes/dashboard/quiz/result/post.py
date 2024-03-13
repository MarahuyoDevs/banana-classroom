from starlette.requests import Request
from starlette.responses import PlainTextResponse
from banana_classroom.database.NOSQL import banana_classroom


async def endpoint(request: Request):

    answer_list = list((await request.json())["answer"])
    quiz_id = request.query_params["quiz_id"]

    quiz = request.state.backend.get(
        f"/quiz/find/?id={quiz_id}",
        headers={
            "Authorization": f"Basic {request.cookies.get('session')}",
        },
    ).json()

    user = request.state.backend.get(
        "/user/me/",
        headers={
            "Authorization": f"Basic {request.cookies.get('session')}",
        },
    )

    answers = {}

    for user_answer, question in zip(answer_list, quiz["questions"]):
        if user_answer.lower() == question["answer"].lower():
            answers[question["id"]] = (
                question["text"],
                question["answer"],
                user_answer,
                True,
            )
        else:
            answers[question["id"]] = (
                question["text"],
                question["answer"],
                user_answer,
                False,
            )

    quiz_result = request.state.backend.post(
        "/quiz/submit/",
        json={"user": user.json(), "quiz": quiz, "answers": answers},
        headers={
            "Authorization": f"Basic {request.cookies.get('session')}",
        },
    )

    return PlainTextResponse(
        "Successfully submitted",
        status_code=200,
        headers={
            "hx-redirect": f"/dashboard/quiz/result/?id={quiz_result.json()['id']}"
        },
    )
