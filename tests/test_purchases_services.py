import pytest
from fastapi import HTTPException
from unittest.mock import patch
from services.purchases_services import getpurchases, addpurchases, clearhistory


class Data():
    supplier = "ABC Traders"
    name = "Nike T-Shirt"
    size = "M"
    quantity = 10
    price = 599.0


class Supplier():
    suid = 1
    name = "ABC Traders"
    phno = "9876543210"


class Purchase():
    puid = 1
    name = "Nike T-Shirt"
    size = "M"
    quantity = 10
    price = 599.0
    suid = 1


# Get Purchases
def test_getpurchases():
    with patch("services.purchases_services.get_purchases") as mock_getpurchases:
            purchase = [Purchase()]
            mock_getpurchases.return_value = purchase
            result = getpurchases(True)
            assert result == {"puchases": purchase}

def test_getpurchases_internalservererror():
    with patch("services.purchases_services.get_purchases") as mock_getpurchases:
            mock_getpurchases.return_value = None
            with pytest.raises(HTTPException) as exc:
                getpurchases(True)
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_getpurchases_notadmin():
    result = getpurchases(False)
    assert result == None


# Add Purchases
def test_addpurchases():
    with patch("services.purchases_services.get_supplier") as mock_getsupplier, \
         patch("services.purchases_services.add_purchase") as mock_addpurchase:
            mock_getsupplier.return_value = Supplier()
            mock_addpurchase.return_value = Purchase()
            result = addpurchases(True, Data())
            assert result == {"message": "Purchase Added"}

def test_addpurchases_suppliernotfound():
    with patch("services.purchases_services.get_supplier") as mock_getsupplier:
            mock_getsupplier.return_value = None
            with pytest.raises(HTTPException) as exc:
                addpurchases(True, Data())
            assert exc.value.status_code == 404
            assert exc.value.detail == "Supplier Not Found"

def test_addpurchases_internalservererror():
    with patch("services.purchases_services.get_supplier") as mock_getsupplier, \
         patch("services.purchases_services.add_purchase") as mock_addpurchase:
            mock_getsupplier.return_value = Supplier()
            mock_addpurchase.return_value = None
            with pytest.raises(HTTPException) as exc:
                addpurchases(True, Data())
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_addpurchases_notadmin():
    result = addpurchases(False, Data())
    assert result == None


# Clear History
def test_clearhistory():
    with patch("services.purchases_services.get_purchases") as mock_getpurchases, \
         patch("services.purchases_services.delete_purchase") as mock_deletepurchase:
            purchase = [Purchase()]
            mock_getpurchases.return_value = purchase
            mock_deletepurchase.return_value = purchase
            result = clearhistory(True)
            assert result == {"message": "purchase history cleared"}

def test_clearhistory_notfound():
    with patch("services.purchases_services.get_purchases") as mock_getpurchases:
            mock_getpurchases.return_value = None
            with pytest.raises(HTTPException) as exc:
                clearhistory(True)
            assert exc.value.status_code == 404
            assert exc.value.detail == "Purchase History Not Found"

def test_clearhistory_internalservererror():
    with patch("services.purchases_services.get_purchases") as mock_getpurchases, \
         patch("services.purchases_services.delete_purchase") as mock_deletepurchase:
            purchase = [Purchase()]
            mock_getpurchases.return_value = purchase
            mock_deletepurchase.return_value = None
            with pytest.raises(HTTPException) as exc:
                clearhistory(True)
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"


