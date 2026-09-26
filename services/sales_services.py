from fastapi import HTTPException
from models.sales import get_sales,add_sales,delete_sales
from models.products import get_products,update_stock
from config.database import SesssionLocal

def getsales(is_auth):
    if is_auth:
        with SesssionLocal() as db:
            sales = get_sales(db)
            return {"sales" : sales}

def addsales(is_auth,data):
    if is_auth:
        with SesssionLocal() as db:
            product = get_products(db,data.name)
            if product == []:
                raise HTTPException(404,detail="Product Not Found")
            if product[0].stock <= 0 :
                raise HTTPException(404,detail="Stock is empty")
            res = add_sales(db,data.name,data.size,data.quantity,data.price)
            res = update_stock(db,product[0].pid,product[0].stock-data.quantity)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"message" : "Sales Added Successfully"}

def deletesales(isadmin):
    if isadmin:
        with SesssionLocal() as db:
            res = delete_sales(db)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"message" : "Sales Deleted Successfully"}

