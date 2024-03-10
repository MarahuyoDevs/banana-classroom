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
from starlette.authentication import requires
from starlette.requests import Request


@requires(["authenticated", "instructor"])
async def endpoint(request: Request):

    classroom_id = request.query_params.get("id", "")

    classroom = Classroom.safe_get(hash_key=classroom_id)
    if not classroom:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Classroom not found")

    if classroom_id not in request.user.classrooms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Classroom not found"
        )

    classroom.delete()
    return PlainTextResponse(
        f"Classroom {classroom.name} deleted", status_code=status.HTTP_204_NO_CONTENT
    )
