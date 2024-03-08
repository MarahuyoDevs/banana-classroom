from pypox.processing.base import processor
from pypox._types import BodyDict,QueryStr
from banana_classroom.database.NOSQL.banana_classroom import Quiz,Question
from datetime import datetime
from starlette.responses import PlainTextResponse,JSONResponse
from starlette import status
from dyntastic import A
from pydantic import BaseModel

class QuizResult(BaseModel):
    user_answer:str
    correct_answer:str
    score:int    

@processor()
async def endpoint(body:BodyDict,quiz_id:QueryStr):
    
    db_quiz = Quiz.safe_get(quiz_id)
    
    if not db_quiz:
        return PlainTextResponse('Quiz not found',status.HTTP_404_NOT_FOUND)
    
    db_quiz.questions = [Question.safe_get(q) for q in db_quiz.questions]
    
    # answer must match the questions
    if len(body['questions']) != len(db_quiz.questions):
        return PlainTextResponse('Invalid number of answers',status.HTTP_400_BAD_REQUEST)
    
    quiz_results = []
        
    for user_question,db_question in zip([Question(x) for x in body['questions']],db_quiz.questions):
        if db_question.answer.lower() != user_question.answer.lower():
            quiz_results.append(QuizResult(user_answer=user_question.answer,correct_answer=db_question.answer,score=0))
        else:
            quiz_results.append(QuizResult(user_answer=user_question.answer,correct_answer=db_question.answer,score=1))
    
    return JSONResponse({"score":sum([x for x in quiz_results if x.score]),"results":[x.model_dump() for x in quiz_results]})
    #