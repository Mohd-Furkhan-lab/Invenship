from fastapi import FastAPI
from routes.user import users
from routes.products import products
from routes.sales import sales
from routes.suppliers import suppliers

app = FastAPI()
app.include_router(users)
app.include_router(products)
app.include_router(sales)
app.include_router(suppliers)
def get_app():
    return app