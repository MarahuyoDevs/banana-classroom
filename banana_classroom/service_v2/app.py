from pypox.application import Pypox
from pypox.router import HTTPRouter
import os
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)

from banana_classroom.database.NOSQL.banana_classroom import User
from base64 import b64decode


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return
        auth = request.headers["Authorization"]
        if not auth.startswith("Basic "):
            return
        try:
            decoded = b64decode(auth.split("Basic ")[1]).decode()
            email, password = decoded.split(":")
            user = User.safe_get(hash_key=email)
            if not user:
                return
            if password != user.password:
                return
            return AuthCredentials(["authenticated", user.role]), user

        except Exception as e:
            raise AuthenticationError("Invalid basic auth credentials")


api_service = Pypox(
    conventions=[HTTPRouter(os.path.dirname(__file__))],
    middleware=[Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())],
)
