from pypox.application import Pypox
from pypox.router import HTTPRouter
import os

api_service = Pypox(conventions=[HTTPRouter(os.path.dirname(__file__))])
