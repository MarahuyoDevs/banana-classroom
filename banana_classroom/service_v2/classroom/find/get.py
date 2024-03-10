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
from starlette.authentication import requires
from starlette.requests import Request
from starlette.exceptions import HTTPException


@requires(["authenticated"])
async def endpoint(request: Request):

    class_id = request.query_params.get("id", "")

    if not request.query_params.get("id", ""):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="id is required"
        )

    if class_id not in request.user.classrooms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Classroom not found"
        )

    classroom = Classroom.safe_get(hash_key=request.query_params.get("id", ""))
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found"
        )

    return JSONResponse(classroom.model_dump())
