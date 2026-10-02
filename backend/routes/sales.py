from fastapi import APIRouter,Depends
from backend.dependecies.sales_users_dependency import require_admin_or_receptionist
from backend.dependecies.admin_dependecy import is_admin
from backend.schemas.sales_schemas import AddSales
from backend.services.sales_services import getsales,addsales,deletesales

sales = APIRouter(prefix="/sales",tags=["sales"])

@sales.get('/')
def get_sales(is_auth = Depends(require_admin_or_receptionist)):
    return getsales(is_auth)

@sales.post('/')
def add_sales(data:AddSales,is_auth = Depends(require_admin_or_receptionist)):
    return addsales(is_auth,data)

@sales.delete('/clear')
def delete_sales(isadmin = Depends(is_admin)):
    return deletesales(isadmin)
