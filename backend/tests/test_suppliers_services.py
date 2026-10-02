import pytest
from fastapi import HTTPException
from unittest.mock import patch
from backend.services.suppliers_services import getsuppliers, addsupplier, removesuppliers


class Data():
    name = "ABC Traders"
    phno = "9876543210"


class Supplier():
    suid = 1
    name = "ABC Traders"
    phno = "9876543210"


# Get Suppliers
def test_getsuppliers():
    with patch("services.suppliers_services.get_supplier") as mock_getsupplier:
            supplier = Supplier()
            mock_getsupplier.return_value = supplier
            result = getsuppliers(True)
            assert result == {"data": supplier}

def test_getsuppliers_notfound():
    with patch("services.suppliers_services.get_supplier") as mock_getsupplier:
            mock_getsupplier.return_value = None
            with pytest.raises(HTTPException) as exc:
                getsuppliers(True)
            assert exc.value.status_code == 404
            assert exc.value.detail == "Not Found"

def test_getsuppliers_notadmin():
    result = getsuppliers(False)
    assert result == None


# Add Supplier
def test_addsupplier():
    with patch("services.suppliers_services.get_supplier") as mock_getsupplier, \
         patch("services.suppliers_services.add_supplier") as mock_addsupplier:
            mock_getsupplier.return_value = None
            mock_addsupplier.return_value = Supplier()
            result = addsupplier(True, Data())
            assert result == {"message": "supplier added successfullt"}

def test_addsupplier_alreadyexists():
    with patch("services.suppliers_services.get_supplier") as mock_getsupplier:
            mock_getsupplier.return_value = Supplier()
            with pytest.raises(HTTPException) as exc:
                addsupplier(True, Data())
            assert exc.value.status_code == 309
            assert exc.value.detail == "Supplier Already Exists"

def test_addsupplier_internalservererror():
    with patch("services.suppliers_services.get_supplier") as mock_getsupplier, \
         patch("services.suppliers_services.add_supplier") as mock_addsupplier:
            mock_getsupplier.return_value = None
            mock_addsupplier.return_value = None
            with pytest.raises(HTTPException) as exc:
                addsupplier(True, Data())
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_addsupplier_notadmin():
    result = addsupplier(False, Data())
    assert result == None


# Remove Supplier
def test_removesuppliers():
    with patch("services.suppliers_services.get_supplier") as mock_getsupplier, \
         patch("services.suppliers_services.remove_supplier") as mock_removesupplier:
            supplier = Supplier()
            mock_getsupplier.return_value = supplier
            mock_removesupplier.return_value = supplier
            result = removesuppliers(True, "ABC Traders")
            assert result == {"message": "supplier deleted successfully"}

def test_removesuppliers_notfound():
    with patch("services.suppliers_services.get_supplier") as mock_getsupplier:
            mock_getsupplier.return_value = None
            with pytest.raises(HTTPException) as exc:
                removesuppliers(True, "ABC Traders")
            assert exc.value.status_code == 404
            assert exc.value.detail == "Supplier Not Found"

def test_removesuppliers_internalservererror():
    with patch("services.suppliers_services.get_supplier") as mock_getsupplier, \
         patch("services.suppliers_services.remove_supplier") as mock_removesupplier:
            supplier = Supplier()
            mock_getsupplier.return_value = supplier
            mock_removesupplier.return_value = None
            with pytest.raises(HTTPException) as exc:
                removesuppliers(True, "ABC Traders")
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_removesuppliers_notadmin():
    result = removesuppliers(False, "ABC Traders")
    assert result == None