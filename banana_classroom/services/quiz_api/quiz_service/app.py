from pypox.application import Pypox
from pypox.router import HTTPRouter
import os

service = Pypox(conventions=[HTTPRouter(os.path.dirname(__file__) + "/resources")])
