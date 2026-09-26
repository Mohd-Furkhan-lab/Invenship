from fastapi import APIRouter,Depends
from schemas.purchases_schemas import AddPurchase
from services.purchases_services import getpurchases,addpurchases,clearhistory
from dependecies.admin_dependecy import is_admin

purchase = APIRouter(prefix="/purchases",tags=["purchases"])

@purchase.get('/')
def fetch_purchases(is_admin = Depends(is_admin)):
    return getpurchases(is_admin)

@purchase.post('/')
def add_purchase(data:AddPurchase,is_admin = Depends(is_admin)):
    return addpurchases(is_admin,data)

@purchase.delete('/')
def clear_purchase_history(is_admin = Depends(is_admin)):
    return clearhistory(is_admin)