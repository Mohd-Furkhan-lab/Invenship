from fastapi import APIRouter,Depends
from backend.schemas.suppliers_schemas import AddSupplier
from backend.services.suppliers_services import getsuppliers,addsupplier,removesuppliers
from backend.dependecies.admin_dependecy import is_admin

suppliers = APIRouter(prefix="/suppliers",tags=["suppliers"])

@suppliers.get('/')
def fetch_suppliers(is_admin = Depends(is_admin),name: str | None = None):
    return getsuppliers(is_admin,name)

@suppliers.post('/')
def add_supplier(data : AddSupplier,is_admin = Depends(is_admin)):
    return addsupplier(is_admin,data)

@suppliers.delete('/{name}')
def remove_supplier(name,is_admin = Depends(is_admin)):
    return removesuppliers(is_admin,name)

