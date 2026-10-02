import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from backend.services.admin_services import getusers, adduser, updaterole, deleteuser


class Data():
    name = "John Doe"
    email = "john@example.com"
    password = "secret123"
    role = "user"


class UpdateData():
    email = "john@example.com"
    new_role = "admin"


class User():
    def get(self, key):
        data = {"uid": 1, "username": "John Doe", "email": "john@example.com"}
        return data.get(key)


def mock_session(mock_sessionlocal):
    mock_db = MagicMock()
    mock_sessionlocal.return_value.__enter__.return_value = mock_db
    return mock_db


# Get Users
def test_getusers():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = User()
            result = getusers(True, "john@example.com")
            assert result == {"data": mock_getuser.return_value}

def test_getusers_internalservererror():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = None
            with pytest.raises(HTTPException) as exc:
                getusers(True, "john@example.com")
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_getusers_notadmin():
    result = getusers(False, "john@example.com")
    assert result == None


# Add User
def test_adduser():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser, \
         patch("services.admin_services.add_user") as mock_adduser:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = None
            mock_adduser.return_value = User()
            result = adduser(True, Data())
            assert result == {"message": "John Doe added succssfully"}

def test_adduser_alreadyexists():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = User()
            with pytest.raises(HTTPException) as exc:
                adduser(True, Data())
            assert exc.value.status_code == 309
            assert exc.value.detail == "User Already Exists"

def test_adduser_internalservererror():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser, \
         patch("services.admin_services.add_user") as mock_adduser:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = None
            mock_adduser.return_value = None
            with pytest.raises(HTTPException) as exc:
                adduser(True, Data())
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_adduser_notadmin():
    result = adduser(False, Data())
    assert result == None


# Update Role
def test_updaterole():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser, \
         patch("services.admin_services.update_role") as mock_updaterole:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = User()
            mock_updaterole.return_value = User()
            result = updaterole(True, UpdateData())
            assert result == {"message": "John Doe updated to admin"}

def test_updaterole_notfound():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = None
            with pytest.raises(HTTPException) as exc:
                updaterole(True, UpdateData())
            assert exc.value.status_code == 404
            assert exc.value.detail == "User Not Found"

def test_updaterole_internalservererror():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser, \
         patch("services.admin_services.update_role") as mock_updaterole:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = User()
            mock_updaterole.return_value = None
            with pytest.raises(HTTPException) as exc:
                updaterole(True, UpdateData())
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_updaterole_notadmin():
    result = updaterole(False, UpdateData())
    assert result == None


# Delete User
def test_deleteuser():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser, \
         patch("services.admin_services.delete_user") as mock_deleteuser:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = User()
            mock_deleteuser.return_value = User()
            result = deleteuser(True, "john@example.com")
            assert result == {"message": "John Doe deleted successfully"}

def test_deleteuser_notfound():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = None
            with pytest.raises(HTTPException) as exc:
                deleteuser(True, "john@example.com")
            assert exc.value.status_code == 404
            assert exc.value.detail == "User Not Found"

def test_deleteuser_internalservererror():
    with patch("services.admin_services.SesssionLocal") as mock_sessionlocal, \
         patch("services.admin_services.get_user") as mock_getuser, \
         patch("services.admin_services.delete_user") as mock_deleteuser:
            mock_session(mock_sessionlocal)
            mock_getuser.return_value = User()
            mock_deleteuser.return_value = None
            with pytest.raises(HTTPException) as exc:
                deleteuser(True, "john@example.com")
            assert exc.value.status_code == 500
            assert exc.value.detail == "Internal Server Error"

def test_deleteuser_notadmin():
    result = deleteuser(False, "john@example.com")
    assert result == None