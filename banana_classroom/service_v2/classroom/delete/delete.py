from banana_classroom.database.NOSQL.banana_classroom import Classroom
from pypox.processing.base import processor
from starlette.exceptions import HTTPException
from starlette.responses import PlainTextResponse
from starlette import status
from pypox._types import BodyDict, QueryStr
from dyntastic import A
from passlib.hash import bcrypt
from datetime import datetime
from pydantic import BaseModel

@processor()
async def endpoint(classroom_name: QueryStr):
    classroom = Classroom.safe_get(hash_key=classroom_name)
    if not classroom:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Classroom not found")
    classroom.delete()
    return PlainTextResponse(f"Classroom {classroom.name} deleted", status_code=status.HTTP_204_NO_CONTENT)
    
