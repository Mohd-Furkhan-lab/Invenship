from fastapi import HTTPException
from models.purchases import get_purchases,add_purchase,delete_purchase
from config.database import SesssionLocal

def getpurchases(is_admin):
    with SesssionLocal() as db:
        res = get_purchases(db)
        if res is None:
            raise HTTPException(500,detail="Internal Server Error")
        return {"puchases" : res}

