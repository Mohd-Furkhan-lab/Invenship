import pytest
from fastapi import HTTPException
from unittest.mock import patch
from backend.services.users_services import getinfo,userlogin,istokenrevoked,changepassword,userlogout,refreshtoken

class Details():
    username = "sohail"
    email = "admin@gmail.com"

User = {
    "uid" : 1,
    "username" : "sohail",
    "email" : "admin@gmail.com",
    "password" : "Mf#@00225588",
    "role" : "admin"
}

class Data(): 
    email = "admin@gmail.com"
    password = "Mf#@00225588"

class Password():
    oldpassword = "Mf#@002255"
    newpassword = "Mf#@002255"

payload = {
     "userid" : 1,
     "role" : "admin",
     "type" : "access",
     "jti" : "asdfasdfffewq"
}

rpayload = {
    "jti": "refresh123",
    "exp": 2000
            }

apayload = {
    "userid": 1,
    "role": "admin",
    "type": "access",
    "jti": "access123",
    "exp": 2000
            }

#User Login
def test_login():
    with patch("backend.services.users_services.get_user")  as mock_get_user , \
         patch("backend.services.users_services.checkpw") as mock_checkpw, \
         patch("backend.services.users_services.create_access_token") as mock_atoken, \
         patch("backend.services.users_services.create_refresh_token") as mock_rtoken : 
            mock_get_user.return_value = User
            mock_checkpw.return_value = True
            mock_atoken.return_value = "afdsbiubopubp598h9  nb9yh hy9h495npohpubhjf"
            mock_rtoken.return_value = "asdf98hg9ing9 n98h3nkjn 98"
            result = userlogin(Data())
            assert result == ["afdsbiubopubp598h9  nb9yh hy9h495npohpubhjf","asdf98hg9ing9 n98h3nkjn 98"]

def test_login_usernotfound():
    with patch("backend.services.users_services.get_user")  as mock_get_user : 
            mock_get_user.return_value = None
            with pytest.raises(HTTPException) as e:
                userlogin(Data())
            assert e.value.status_code == 404
            assert e.value.detail == "User Not Found"

def test_login_invalidcredentails():
    with patch("backend.services.users_services.get_user")  as mock_get_user , \
         patch("backend.services.users_services.checkpw") as mock_checkpw : 
            mock_get_user.return_value = User
            mock_checkpw.return_value = False
            with pytest.raises(HTTPException) as e:
                userlogin(Data())
            assert e.value.status_code == 401
            assert e.value.detail == "Invalid Credentials"

#Toekn Checker
def test_istokenrevoked_access():
    with patch("backend.services.users_services.r.get") as mock_rget , \
         patch("backend.services.users_services.is_revoked") as mock_is_revoked :
            mock_rget.return_value = "1"
            mock_is_revoked.return_value = None
            with pytest.raises(HTTPException) as e:
                   istokenrevoked("db","1")
            assert e.value.status_code == 401
            assert e.value.detail == "Token Revoked"

def test_istokenrevoked_refresh():
    with patch("backend.services.users_services.r.get") as mock_rget , \
         patch("backend.services.users_services.is_revoked") as mock_is_revoked :
            mock_rget.return_value = None
            mock_is_revoked.return_value = "asdfasdfasdf"
            with pytest.raises(HTTPException) as e:
                   istokenrevoked("db","1")
            assert e.value.status_code == 401
            assert e.value.detail == "Token Revoked"

#User Info
def test_get_details():
    with patch("backend.services.users_services.get_details") as mock_get_user, \
         patch("backend.services.users_services.istokenrevoked") as mock_isrevoekd:
            user = Details()
            mock_get_user.return_value = user
            mock_isrevoekd.return_value = None
            result = getinfo(payload)
            assert result == {"details" : user}

def test_get_details_usernotfound():
    with patch("backend.services.users_services.get_details") as mock_get_user, \
         patch("backend.services.users_services.istokenrevoked") as mock_isrevoekd:
            mock_get_user.return_value = None
            mock_isrevoekd.return_value = None
            with pytest.raises(HTTPException) as e:
                getinfo(payload)
            assert e.value.status_code == 404
            assert e.value.detail == "User Not Found"

def test_get_details_revokedtoken():
    with patch("backend.services.users_services.get_details") as mock_get_user, \
         patch("backend.services.users_services.istokenrevoked") as mock_isrevoekd:
            user = Details()
            mock_get_user.return_value = user
            mock_isrevoekd.side_effect = HTTPException(401,detail = "Token Revoked")
            with pytest.raises(HTTPException) as e:
                getinfo(payload)
            assert e.value.status_code == 401
            assert e.value.detail == "Token Revoked"
            
#User Change Password
def test_changepassword():
    with patch("backend.services.users_services.istokenrevoked") as mock_tokenrevoked , \
         patch("backend.services.users_services.get_user") as mock_getuser , \
         patch("backend.services.users_services.checkpw") as mock_checkpw , \
         patch("backend.services.users_services.hashpw") as mock_hashpw , \
         patch("backend.services.users_services.change_password") as mock_change_password :
            mock_tokenrevoked.return_value = None
            mock_getuser.return_value = User
            mock_checkpw.return_value = True
            mock_hashpw.return_value = b"$2b$12$somevalidlookinghash"
            mock_change_password.return_value = User
            result = changepassword(Password(),payload)
            assert result == {"message" : "passowrd updated successfully"}

def test_changepassword_usernotfound():
    with patch("backend.services.users_services.istokenrevoked") as mock_tokenrevoked , \
         patch("backend.services.users_services.get_user") as mock_getuser :
            mock_tokenrevoked.return_value = None
            mock_getuser.return_value = None
            with pytest.raises(HTTPException) as e:
                changepassword(Password(),payload)
            assert e.value.status_code == 404
            assert e.value.detail == "User Not Found"

def test_changepassword_wrongcredentails():
    with patch("backend.services.users_services.istokenrevoked") as mock_tokenrevoked , \
         patch("backend.services.users_services.get_user") as mock_getuser , \
         patch("backend.services.users_services.checkpw") as mock_checkpw :
            mock_tokenrevoked.return_value = None
            mock_getuser.return_value = User
            mock_checkpw.return_value = False
            with pytest.raises(HTTPException) as e:
                  changepassword(Password(),payload)
            assert e.value.status_code == 401
            assert e.value.detail == "Invalid Old Password"

def test_changepassword_internalservererror():
    with patch("backend.services.users_services.istokenrevoked") as mock_tokenrevoked , \
         patch("backend.services.users_services.get_user") as mock_getuser , \
         patch("backend.services.users_services.checkpw") as mock_checkpw , \
         patch("backend.services.users_services.hashpw") as mock_hashpw , \
         patch("backend.services.users_services.change_password") as mock_change_password :
            mock_tokenrevoked.return_value = None
            mock_getuser.return_value = User
            mock_checkpw.return_value = True
            mock_hashpw.return_value = b"$2b$12$somevalidlookinghash"
            mock_change_password.return_value = None
            with pytest.raises(HTTPException) as e:
                changepassword(Password(),payload)
            assert e.value.status_code == 500
            assert e.value.detail == "Internal Server Error"

# User Logout
def test_userlogout():
    with patch("backend.services.users_services.r.set") as mock_rset, \
         patch("backend.services.users_services.revoketoken") as mock_revoketoken, \
         patch("backend.services.users_services.time.time") as mock_time:

            mock_time.return_value = 1000
            mock_rset.return_value = True
            mock_revoketoken.return_value = "token revoked"

            rpayload = {
                "jti": "refresh123",
                "exp": 2000
            }

            apayload = {
                "userid": 1,
                "role": "admin",
                "type": "access",
                "jti": "access123",
                "exp": 2000
            }

            result = userlogout(rpayload, apayload)

            assert result == {"message": "logout successfully"}


def test_userlogout_internalservererror():
    with patch("backend.services.users_services.r.set") as mock_rset, \
         patch("backend.services.users_services.revoketoken") as mock_revoketoken, \
         patch("backend.services.users_services.time.time") as mock_time:
            mock_time.return_value = 1000
            mock_rset.return_value = True
            mock_revoketoken.return_value = None
            with pytest.raises(HTTPException) as e:
                userlogout(rpayload, apayload)
            assert e.value.status_code == 500
            assert e.value.detail == "Internal Server Error"

# Refresh Token
def test_refreshtoken():
    with patch("backend.services.users_services.istokenrevoked") as mock_tokenrevoked, \
         patch("backend.services.users_services.create_access_token") as mock_atoken:
            mock_tokenrevoked.return_value = None
            mock_atoken.return_value = "new_access_token"
            result = refreshtoken(rpayload)
            assert result == "new_access_token"


def test_refreshtoken_internalservererror():
    with patch("backend.services.users_services.istokenrevoked") as mock_tokenrevoked, \
         patch("backend.services.users_services.create_access_token") as mock_atoken:
            mock_tokenrevoked.return_value = None
            mock_atoken.return_value = None
            with pytest.raises(HTTPException) as e:
                refreshtoken(rpayload)
            assert e.value.status_code == 500
            assert e.value.detail == "Internal Server Error"