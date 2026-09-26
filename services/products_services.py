from models.products import get_products,add_product,update_product_details,delete_product
from models.category import get_category,add_category,delete_category,get_all_categories
from config.database import SesssionLocal
from fastapi import HTTPException
from cloudinary import uploader

def getproducts(isadmin,name,brand,size):
    if isadmin:
        with SesssionLocal() as db:
            products = get_products(db,name,brand,size)
            return {"products" : products}

def imguploader(isadmin,file):
    if isadmin:
        upload = uploader.upload(file.file,resource_type="auto")
        return upload.get("secure_url")

def getcategories(isadmin):
    if isadmin:
        with SesssionLocal() as db:
            categories = get_all_categories(db)
            return {"categories" : categories}

def addcategory(isadmin,name):
    if isadmin:
        with SesssionLocal() as db:
            isexisting = get_category(db,name)
            if isexisting:
                raise HTTPException(309,detail="Category Already Exists")
            res = add_category(db,name)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"message" : f"{name} added successfully"}

def deletecategory(isadmin,name):
    if isadmin:
        with SesssionLocal() as db:
            category = get_category(db,name)
            if category is None:
                raise HTTPException(404,detail="Category Not Found")
            res = delete_category(db,category.cid)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"message" : f"{name} deleted successfully"}

def addproduct(isadmin,data):
    if isadmin:
        with SesssionLocal() as db:
            category = get_category(db,data.category)
            if category is None:
                raise HTTPException(404,detail="Category Not Found")
            is_existing = get_products(db,data.name,data.brand,data.size)
            if is_existing:
                raise HTTPException(309,detail="Product Already Exists")
            res = add_product(db,category.cid,data.name,data.url,data.size,data.brand,data.price,data.stock)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"mesage" : f"{data.name} added successfully"}

def updateproduct(isadmin,data,name):
    if isadmin:
        with SesssionLocal() as db:
            product = get_products(db,name)
            if product == []:
                raise HTTPException(404,detail="Product Not Found")
            res = update_product_details(db,product[0].pid,data.price,data.stock)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"mesage" : f"{product[0].pname} details updated successfully"}

def deleteproduct(isadmin,name):
    if isadmin:
        with SesssionLocal() as db:
            prodcut = get_products(db,name)
            if prodcut is None:
                raise HTTPException(404,detail="Product Not Found")
            res = delete_product(db,prodcut[0].pid)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"message" : f"{name} deleted successfully"}      
                 
