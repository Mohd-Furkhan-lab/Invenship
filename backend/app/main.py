from fastapi import FastAPI
from backend.routes.users import users
from backend.routes.products import products
from backend.routes.sales import sales
from backend.routes.suppliers import suppliers
from backend.routes.purchases import purchase
from backend.routes.admin import admin
from backend.routes.analysis import analysis

app = FastAPI()
app.include_router(users)
app.include_router(analysis)
app.include_router(admin)
app.include_router(products)
app.include_router(sales)
app.include_router(suppliers)
app.include_router(purchase)
def get_app():
    return app