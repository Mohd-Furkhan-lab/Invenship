from fastapi import APIRouter,Depends
from dependecies.admin_dependecy import is_admin
from services.product_services import getproducts,addproduct,updateproduct,deleteproduct,imguploader,addcategory,deletecategory
from schemas.product_schemas import GetProducts,AddProduct,UpdateProducts

products = APIRouter(prefix="/products",tags=["products"])

@products.get('/')
def fetch_products(data : GetProducts,isadmin = Depends(is_admin)):
    return getproducts(isadmin,data)

@products.post('/')
def add_product(data:AddProduct,isadmin = Depends(is_admin)):
    return addproduct(isadmin,data)

@products.put('/{name}')
def update_products(name,data:updateproduct,isadmin = Depends(is_admin)):
    return updateproduct(isadmin,data,name)

@products.delete('/{name}')
def delete_product(name,isadmin = Depends(is_admin)):
    return deleteproduct(isadmin,name)

@products.post('/category/{name}')
def add_category(name,isadmin = Depends(is_admin)):
    return addcategory(isadmin,name)

@products.delete('/category/{name}')
def delete_category(name,isadmin = Depends(is_admin)):
    return deletecategory(isadmin,name)

