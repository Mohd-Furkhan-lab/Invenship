from fastapi import HTTPException
from unittest.mock import patch
import pytest
from backend.services.sales_services import getsales,addsales,deletesales

class Data():
    name="Nike T-Shirt"
    size="M"
    quantity=2
    price=599.0

class Sales():
    sid=1
    pname="Nike T-Shirt"
    size="M"
    quantity=2
    price=999.0
    total=1198.0
    timestamp="2026-09-24 18:10:00+00:00"

class Product():
    pid = 1
    pname = "Nike T-Shirt"
    brand = "Nike"
    size = "M"
    price = 999.0
    stock = 20

#GetSales
def test_getsales():
    with patch("services.sales_services.get_sales") as mock_getsales:
        sales = Sales()
        mock_getsales.return_value = sales
        result = getsales(True)
        assert result == {"sales" : sales}

def test_getsales_notadmin():
    result = getsales(False)
    assert result == None

#AddSales
def test_addsales():
    with patch("services.sales_services.get_products") as mock_getproducts, \
         patch("services.sales_services.add_sales") as mock_addproducts, \
         patch("services.sales_services.update_stock") as mock_updatestock :
            product = [Product()]
            mock_getproducts.return_value = product
            mock_addproducts.return_value = Sales()
            mock_updatestock.return_value = product
            result = addsales(True,Data())
            assert result == {"message" : "Sales Added Successfully"}

def test_addsales_prodcut_notfound():
    with patch("services.sales_services.get_products") as mock_getproducts:
            mock_getproducts.return_value = []
            with pytest.raises(HTTPException) as exc:
                addsales(True,Data())
            assert exc.value.status_code == 404
            assert exc.value.detail == "Product Not Found"

def test_addsales_emptystock():
    with patch("services.sales_services.get_products") as mock_getproducts:
            product = [Product()]
            product[0].stock = 0 
            mock_getproducts.return_value = product
            with pytest.raises(HTTPException) as exc:
                addsales(True,Data())
            assert exc.value.status_code == 404
            assert exc.value.detail == "Stock is empty"

def test_addsales_internalservererror():
    with patch("services.sales_services.get_products") as mock_getproducts, \
         patch("services.sales_services.add_sales") as mock_addproducts, \
         patch("services.sales_services.update_stock") as mock_updatestock :
            product = [Product()]
            mock_getproducts.return_value = product
            mock_addproducts.return_value = None
            mock_updatestock.return_value = None
            with pytest.raises(HTTPException) as exc:
                addsales(True,Data())
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_addsales_notadmin():
    result = addsales(False,Data())
    assert result == None

#DeleteSales
def test_deletesales():
    with patch("services.sales_services.delete_sales") as mock_deletesales:
        mock_deletesales.return_value = Product()
        res = deletesales(True)
        assert res == {"message" : "Sales Deleted Successfully"} 

def test_deletesales_internalservererror():
    with patch("services.sales_services.delete_sales") as mock_deletesales:
        mock_deletesales.return_value = None
        with pytest.raises(HTTPException) as exc:
            deletesales(True)
        assert exc.value.status_code == 500
        assert exc.value.detail == "Internal Server Error"

def test_deletesales_notadmin():
    result = deletesales(False)
    assert result == None