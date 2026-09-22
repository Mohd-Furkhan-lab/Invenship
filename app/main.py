from fastapi import FastAPI
from routes.user import users

app = FastAPI()
app.include_router(users)
def get_app():
    return app