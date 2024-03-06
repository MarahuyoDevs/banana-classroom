import os
from pypox.application import PypoxHTMX
from starlette.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware

template = Jinja2Templates(os.path.dirname(__file__) + "/templates/")

frontend_app = PypoxHTMX(os.path.dirname(__file__) + "/routes")
