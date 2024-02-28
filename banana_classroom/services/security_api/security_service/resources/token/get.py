from pypox.processing import processor, BodyDict
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from banana_classroom.services.user_api.user_service.databases.NOSQL.userNOSQL import (
    User,
)
from passlib.hash import pbkdf2_sha256
from jose import jwt
import os


@processor
async def endpoint(body: BodyDict):
    # check if user in the database
    user = User.safe_get(hash_key=body["email"])
    if not user or pbkdf2_sha256.verify(body["password"], user.password):
        raise HTTPException(400, "Invalid email or password")
    # generate token
    token = jwt.encode(
        user.model_dump(), os.environ.get("JWT_SECRET", ""), algorithm="HS256"
    )

    return JSONResponse(
        {"access_token": token, "token_type": "bearer", "scopes": user.scopes}
    )
