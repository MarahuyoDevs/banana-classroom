from mangum import Mangum
from starlette.applications import Starlette
from banana_classroom.services.quiz_api.quiz_service.app import service as quiz_api
from banana_classroom.services.user_service.app import service as user_api

app = Starlette()

app.mount("/api/user/", user_api, name="user")
app.mount("/api/", quiz_api, name="quiz")

handler = Mangum(app)
