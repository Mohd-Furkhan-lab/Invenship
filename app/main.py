from fastapi import FastAPI
from routes.users import users
from routes.products import products
from routes.sales import sales
from routes.suppliers import suppliers
from routes.purchases import purchase

app = FastAPI()
app.include_router(users)
app.include_router(products)
app.include_router(sales)
app.include_router(suppliers)
app.include_router(purchase)
def get_app():
    return app