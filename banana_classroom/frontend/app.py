import os
from pypox.application import PypoxHTMX

frontend_app = PypoxHTMX(os.path.dirname(__file__) + "/routes")
