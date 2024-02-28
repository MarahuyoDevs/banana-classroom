from pypox.router import HTTPRouter
from pypox.application import Pypox
from pypox.authentication import BearerTokenMiddleware
from starlette.applications import Starlette
import os

service = Pypox(
    conventions=[HTTPRouter(os.path.dirname(__file__) + "/resources/me")],
)
