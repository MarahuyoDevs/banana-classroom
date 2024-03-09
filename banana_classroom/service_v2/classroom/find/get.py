from banana_classroom.database.NOSQL.banana_classroom import Classroom
from pypox.processing.base import processor
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette import status
from pypox._types import BodyDict, QueryStr
from dyntastic import A
from passlib.hash import bcrypt
from datetime import datetime
from pydantic import BaseModel

@processor()
async def endpoint(classroom_name: QueryStr):
    classroom = Classroom.safe_get(classroom_name)
    if not classroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found")

    return JSONResponse(classroom.model_dump())