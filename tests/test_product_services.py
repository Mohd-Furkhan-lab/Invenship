import pytest
from fastapi import HTTPException
from unittest.mock import patch
from services.products_services import getproducts,addproduct,updateproduct,deleteproduct,getcategories,addcategory,deletecategory,imguploader

class Data():
    name = "Nike T-Shirt"
    brand = "Nike"
    size = "M"
    category = "T-Shirts"
    url = "https://example.com/image.jpg"
    price = 999
    stock = 20

UploadedFile = {
    "secure_url" :  "https://example.com/image.jpg"
}

class UpdateData():
    price = 899
    stock = 15


class File():
    file = "dummy_file"


class Category():
    cid = 1
    name = "T-Shirts"


class Product():
    pid = 1
    pname = "Nike T-Shirt"
    brand = "Nike"
    size = "M"
    price = 999
    stock = 20

#Get Products
def test_getproducts():
    with patch("services.product_services.get_products") as mock_products:
        product = [Product()]
        mock_products.return_value = product
        result = getproducts(True,Data())
        assert result == {"products" : product} 

def test_getproducts_noadmin():
    result =  getproducts(False,Data)
    assert result == None

#Add Products
def test_addproducts():
    with patch("services.product_services.get_category") as mock_getcategory, \
         patch("services.product_services.get_products") as mock_getproducts, \
         patch("services.product_services.add_product") as mock_addproduct :
            mock_getcategory.return_value = Category()
            mock_getproducts.return_value = None
            mock_addproduct.return_value = Product()
            result = addproduct(True,Data())
            assert result == {"mesage" : "Nike T-Shirt added successfully"}

def test_addproducts_categorynotfound():
    with patch("services.product_services.get_category") as mock_getcategory :
            mock_getcategory.return_value = None
            with pytest.raises(HTTPException) as exc:
                addproduct(True,Data())
            assert exc.value.status_code == 404
            assert exc.value.detail == "Category Not Found"

def test_addproducts_productalreadyexsists():
    with patch("services.product_services.get_category") as mock_getcategory, \
         patch("services.product_services.get_products") as mock_getproducts:
            mock_getcategory.return_value = Category()
            mock_getproducts.return_value = Product()
            with pytest.raises(HTTPException) as exc:
                addproduct(True,Data())
            assert exc.value.status_code == 309
            assert exc.value.detail == "Product Already Exists"

def test_addproducts_internalservererror():
    with patch("services.product_services.get_category") as mock_getcategory, \
         patch("services.product_services.get_products") as mock_getproducts, \
         patch("services.product_services.add_product") as mock_addproduct :
            mock_getcategory.return_value = Category()
            mock_getproducts.return_value = None
            mock_addproduct.return_value = None
            with pytest.raises(HTTPException) as exc:
                addproduct(True,Data())
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_addproducts_noadmin():
    result =  addproduct(False,Data())
    assert result == None

#Update Products
def test_updateproduct():
    with patch("services.product_services.get_products") as mock_getproducts, \
         patch("services.product_services.update_product_details") as mock_udpateproduct :
            mock_getproducts.return_value = [Product()]
            mock_udpateproduct.return_value = [Product()]
            result = updateproduct(True,UpdateData(),"Nike T-Shirt")
            assert result == {"mesage" : "Nike T-Shirt details updated successfully"}

def test_updateproduct_notfound():
    with patch("services.product_services.get_products") as mock_getproducts :
            mock_getproducts.return_value = []
            with pytest.raises(HTTPException) as exc:
                updateproduct(True,UpdateData(),"Nike T-Shirt")
            assert exc.value.status_code == 404
            assert exc.value.detail == "Product Not Found"

def test_updateproduct_internalservererror():
    with patch("services.product_services.get_products") as mock_getproducts, \
         patch("services.product_services.update_product_details") as mock_udpateproduct :
            mock_getproducts.return_value = [Product()]
            mock_udpateproduct.return_value = None
            with pytest.raises(HTTPException) as exc:
                updateproduct(True,UpdateData(),"Nike T-Shirt")
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_updateproduct_notadmin():
    res = updateproduct(False,Data,"Nike T-Shirt")
    assert res == None

#Delete Product
def test_deleteproduct():
    with patch("services.product_services.get_products") as mock_getproducts, \
         patch("services.product_services.delete_product") as mock_deletepprodcut :
            product = [Product()]
            mock_getproducts.return_value = product
            mock_deletepprodcut.return_value = product
            res = deleteproduct(True,"Nike T-Shirt")
            assert res == {"message" : "Nike T-Shirt deleted successfully"}

def test_deleteproduct_productnotfound():
    with patch("services.product_services.get_products") as mock_getproducts:
            mock_getproducts.return_value = None
            with pytest.raises(HTTPException) as exc:
                deleteproduct(True,"Nike T-Shirt")
            assert exc.value.status_code == 404
            assert exc.value.detail == "Product Not Found"

def test_deleteproduct_internalservererror():
    with patch("services.product_services.get_products") as mock_getproducts, \
         patch("services.product_services.delete_product") as mock_deletepprodcut :
            product = [Product()]
            mock_getproducts.return_value = product
            mock_deletepprodcut.return_value = None
            with pytest.raises(HTTPException) as exc:
                deleteproduct(True,"Nike T-Shirt")
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_deleteproduct_notadmin():
    res = deleteproduct(False,"Nike T-Shirt")
    assert res == None

#Get Category
def test_getcategories():
    with patch("services.product_services.get_all_categories") as mock_getcategories :
            category = Category()
            mock_getcategories.return_value = category
            res = getcategories(True)
            assert res == {"categories" : category}

def test_getcategories_notadmin():
    res = getcategories(False)
    assert res == None

#Add category
def test_addcategory():
    with patch("services.product_services.get_category") as mock_getcategory, \
         patch("services.product_services.add_category") as mock_addcategory :
            mock_getcategory.return_value = None
            mock_addcategory.return_value = Category()
            res = addcategory(True,"shirt")
            assert res == {"message" : "shirt added successfully"}

def test_addcategory_alreadyexists():
    with patch("services.product_services.get_category") as mock_getcategory :
            mock_getcategory.return_value = Category
            with pytest.raises(HTTPException) as exc:
                addcategory(True,"shirt")
            assert exc.value.status_code == 309
            assert exc.value.detail == "Category Already Exists"

def test_addcategory_internalservererror():
    with patch("services.product_services.get_category") as mock_getcategory, \
         patch("services.product_services.add_category") as mock_addcategory :
            mock_getcategory.return_value = None
            mock_addcategory.return_value = None
            with pytest.raises(HTTPException) as exc :
                addcategory(True,"jeans")
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_addcategory_notadmin():
    res = addcategory(False,"tshirts")
    assert res == None

#Delete Category
def test_deletecategory():
    with patch("services.product_services.get_category") as mock_get_category, \
         patch("services.product_services.delete_category") as mock_deletecategory :
            mock_get_category.return_value = Category()
            mock_deletecategory.return_value = Category()
            res = deletecategory(True,"jeans")
            assert res == {"message" : "jeans deleted successfully"}

def test_deletecategory_notfound():
    with patch("services.product_services.get_category") as mock_get_category :
            mock_get_category.return_value = None
            with pytest.raises(HTTPException) as exc:
                deletecategory(True,"jeans")
            assert exc.value.status_code == 404
            assert exc.value.detail == "Category Not Found"

def test_deletecategory_internalservererror():
    with patch("services.product_services.get_category") as mock_get_category, \
         patch("services.product_services.delete_category") as mock_deletecategory :
            mock_get_category.return_value = Category()
            mock_deletecategory.return_value = None
            with pytest.raises(HTTPException) as exc:
                deletecategory(True,"jeans")
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_delete_notadmin():
    res = deletecategory(False,"tshirts")
    assert res == None

#Img Uploader
def test_imageuploader():
    with patch("services.product_services.uploader.upload") as mock_upload:
        mock_upload.return_value = UploadedFile
        res = imguploader(True,File())
        print(res)
        assert res == "https://example.com/image.jpg"

def test_imageuploader_notadmin():
    res = imguploader(False,File())
    assert res == None