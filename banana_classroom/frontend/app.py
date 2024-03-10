import os
from pypox.application import Pypox
from pypox.router import HTTPRouter
from starlette.templating import Jinja2Templates
from starlette.exceptions import HTTPException

template = Jinja2Templates(os.path.dirname(__file__) + "/templates/")

frontend_app = Pypox([HTTPRouter(os.path.dirname(__file__) + "/routes")])
