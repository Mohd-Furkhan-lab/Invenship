from fastapi import HTTPException
from models.purchases import get_purchases,add_purchase,delete_purchase
from models.suppliers import get_supplier
from config.database import SesssionLocal


def getpurchases(is_admin):
    if is_admin:
        with SesssionLocal() as db:
            res = get_purchases(db)
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
        return {"puchases" : res}

def addpurchases(is_admin,data):
    if is_admin:
        with SesssionLocal() as db:
            supplier = get_supplier(db,data.supplier)
            if supplier is None:
                raise HTTPException(404,detail="Supplier Not Found")
            res = add_purchase(db,data.name,data.size,data.quantity,data.price,supplier.suid)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
        return {"message" : "Purchase Added"}

def clearhistory(is_admin):
    if is_admin:
        with SesssionLocal() as db:
            purchase = get_purchases(db)
            if purchase is None:
                raise HTTPException(404,detail="Purchase History Not Found")
            res = delete_purchase(db)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"message" : "purchase history cleared"}