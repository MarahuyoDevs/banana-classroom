from typing import Optional
from pypox.processing import processor, PathStr, BodyDict
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from banana_classroom.services.quiz_api.quiz_service.database.NOSQL.quizNOSQL import (
    Classroom,
    Question,
    Quiz,
    QuizResult,
)


@processor
async def endpoint(body: BodyDict):

    classroom = Classroom.safe_get(body["class_id"])

    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    if not classroom.quizzes:
        raise HTTPException(status_code=404, detail="No quizzes found")

    latest_quiz: Optional[Quiz] = [
        x for x in classroom.quizzes if x.id == body["quiz_id"]
    ][0]

    if not latest_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    user_quiz = QuizResult(
        title=latest_quiz.title,
        description=latest_quiz.description,
        instructor=latest_quiz.instructor,
        score=0,
    )

    for answer in body["answers"]:  # answers is completed by the user

        for question in latest_quiz.questions:

            if not user_quiz.questions:
                user_quiz.questions = []

            if question.id != answer["question_id"]:
                continue

            if question.answer == answer["answer"]:
                user_quiz.questions.append((question.description, True))
            else:
                user_quiz.questions.append((question.description, False))

            break

    if user_quiz.questions:
        user_quiz.score = len([x for x in user_quiz.questions if x])

    return JSONResponse(user_quiz.model_dump())
