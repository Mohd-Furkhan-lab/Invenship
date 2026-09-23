from fastapi import FastAPI
from routes.user import users
from routes.products import products

app = FastAPI()
app.include_router(users)
app.include_router(products)
def get_app():
    return app