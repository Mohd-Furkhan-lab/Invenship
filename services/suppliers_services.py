from models.suppliers import get_supplier,add_supplier,remove_supplier
from config.database import SesssionLocal
from fastapi import HTTPException

def getsuppliers(is_admin,name = None):
    if is_admin:
        with SesssionLocal() as db:
            data = get_supplier(db,name)
            if data is None:
                raise HTTPException(404,detail="Not Found")
        return {"data" : data}

def addsupplier(is_admin,data):
    if is_admin:
        with SesssionLocal() as db:
            supplier = get_supplier(db,name = data.name)
            if supplier:
                raise HTTPException(309,detail="Supplier Already Exists")
            res = add_supplier(db,data.name,data.phno)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
        return {"message" : "supplier added successfullt"}

def removesuppliers(is_admin,name):
    if is_admin:
        with SesssionLocal() as db:
            supplier = get_supplier(db,name = name)
            if supplier is None:
                raise HTTPException(404,detail="Supplier Not Found")
            res = remove_supplier(db,supplier.suid)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
        return {"message" : "supplier deleted successfully"}

