from fastapi import APIRouter,Depends,UploadFile,File
from dependecies.admin_dependecy import is_admin
from services.products_services import getproducts,addproduct,updateproduct,deleteproduct,imguploader,addcategory,deletecategory,getcategories
from schemas.product_schemas import AddProduct,UpdateProducts

products = APIRouter(prefix="/products",tags=["products"])

@products.get('/')
def fetch_products(name: str | None = None,brand: str | None = None,size: str | None = None,isadmin = Depends(is_admin)):
    return getproducts(isadmin,name,brand,size)

@products.post('/')
def add_product(data:AddProduct,isadmin = Depends(is_admin)):
    return addproduct(isadmin,data)

@products.post('/upload')
def upload_productimg(isadmin = Depends(is_admin),file : UploadFile = File(...)):
    return imguploader(isadmin,file)

@products.put('/{name}')
def update_products(name,data:UpdateProducts,isadmin = Depends(is_admin)):
    return updateproduct(isadmin,data,name)

@products.delete('/{name}')
def delete_product(name,isadmin = Depends(is_admin)):
    return deleteproduct(isadmin,name)

@products.get('/category/')
def getallcategories(isadmin = Depends(is_admin)):
    return getcategories(isadmin)

@products.post('/category/{name}')
def add_category(name,isadmin = Depends(is_admin)):
    return addcategory(isadmin,name)

@products.delete('/category/{name}')
def delete_category(name,isadmin = Depends(is_admin)):
    return deletecategory(isadmin,name)

