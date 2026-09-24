from fastapi import HTTPException
from models.sales import get_sales,add_sales,delete_sales
from config.database import SesssionLocal

def getsales(is_auth):
    if is_auth:
        with SesssionLocal() as db:
            sales = get_sales(db)
            return {"sales" : sales}

def addsales(is_auth,data):
    if is_auth:
        with SesssionLocal() as db:
            res = add_sales(db,data.name,data.size,data.quantity,data.price)
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"message" : "Sales Added Successfully"}

def deletesales(is_auth):
    if is_auth:
        with SesssionLocal() as db:
            res = delete_sales(db)
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"message" : "Sales Deleted Successfully"}
