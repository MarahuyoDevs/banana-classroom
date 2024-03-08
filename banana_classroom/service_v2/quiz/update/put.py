from pypox.processing.base import processor
from pypox._types import BodyDict,QueryStr
from banana_classroom.database.NOSQL.banana_classroom import Quiz,Question
from datetime import datetime
from starlette.responses import PlainTextResponse
from starlette import status
from dyntastic import A
@processor()
async def endpoint(body:BodyDict,classroom_id:QueryStr,quiz_id:QueryStr): 
    
    quiz = Quiz.safe_get(quiz_id)
    
    quiz.update(A.name.set(body.get('name',None) or quiz.name))
    quiz.update(A.description.set(body.get('description',None) or quiz.description))
    
    for question in list(Question(**x) for x in body.get('questions',[])):
        db_question = Question.safe_get(question.id)
        if not db_question:
            continue 
        with Question.batch_writer():      
            db_question.update(A.question.set(question.type or db_question.type))
            db_question.update(A.text.set(question.text or db_question.text))
            db_question.update(A.index.set(question.index or db_question.index))
            db_question.update(A.answer.set(question.answer or db_question.answer))
            db_question.update(A.options.set(question.options or db_question.options))
    quiz.update(A.updated_at.set(str(datetime.now())))

    return PlainTextResponse("Quiz updated successfully", status_code=status.HTTP_202_ACCEPTED)