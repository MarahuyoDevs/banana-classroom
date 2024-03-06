from mangum import Mangum
from starlette.applications import Starlette
from banana_classroom.service_v2.app import api_service
from banana_classroom.frontend.app import frontend_app

app = Starlette()

app.mount("/api/v1/", api_service, name="api")
app.mount("/", frontend_app, name="frontend")

handler = Mangum(app)
