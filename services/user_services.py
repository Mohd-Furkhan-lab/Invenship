from fastapi import HTTPException
from models.user import get_details,get_user,change_password
from models.revoked_token import revoketoken,is_revoked
from auth.token import create_access_token,create_refresh_token
from bcrypt import checkpw,hashpw,gensalt
from config.database import SesssionLocal
from config.redis import r
import time

def userlogin(data):
    with SesssionLocal() as db:
        email,password = data.email,data.password
        user = get_user(db,email)
        if user  is None:
            raise HTTPException(404,detail="User Not Found")
        auth = checkpw(password.encode("utf-8"),user.password.encode('utf-8'))
        if auth is None:
            raise HTTPException(401,detail="Invalid Credentials")
        access_token = create_access_token(user.uid,user.role)
        refresh_token = create_refresh_token(user.uid,user.role)
        return {"tokens" : {"access" : access_token, "refresh" : refresh_token}}

def istokenrevoked(db,jit):
    if r.get(f"blacklist:{jit}"):
        raise HTTPException(401,detail="Token Revoked")
    ispresent = is_revoked(db,jit)
    if ispresent:
        raise HTTPException(401,detail="Token Revoked")

def getinfo(payload):
    if payload is None:
            raise HTTPException(401,detail="Auth Payload Missing")
    with SesssionLocal() as db:
        istokenrevoked(db,payload.get("jti"))
        details = get_details(db,payload.get("userid"))
        if details is None:
            raise HTTPException(404,detail="User Not Found")
        return {"details" : details}

def changepassword(data,payload):
    if payload is None:
        raise HTTPException(401,detail="Auth Payload Missing")
    with SesssionLocal() as db :
        istokenrevoked(db,payload.get("jti"))
        user = get_details(db,payload.get("userid"))
        if user is None:
            raise HTTPException(404,detail = "User Not Found")
        old_password,new_password = data.oldpassword,data.newpassword
        is_valid_password = checkpw(old_password.encode('utf-8'),user.password.encode('utf-8'))
        if is_valid_password is None:
            raise HTTPException(401,detail="Invalid Old Password")
        new_hash = hashpw(new_password.encode('utf-8'),gensalt())
        res = change_password(db,payload.get("userid"),new_hash)
        db.commit()
        if res is None:
            raise HTTPException(500,detail="Internal Server Error") 
        return {"message" : "passowrd updated successfully"}

def userlogout(rpayload,apayload):
    with SesssionLocal() as db:
        remaining_time = apayload.get("exp") - int(time.time())
        r.set(f"blacklist:{apayload.get("jti")}",1,remaining_time)
        res = revoketoken(db,rpayload.get("jti"),rpayload.get("exp"),True)
        if res is None:
            raise HTTPException(500,detail="Internal Server Error")
        db.commit()
        return {"message" : "logout successfully"}

def refreshtoken(rpayload):
    with SesssionLocal() as db:
        istokenrevoked(db,rpayload.get("jti"))
        new_token = create_access_token(rpayload.get("userid"),rpayload.get("role"))
        if new_token is None:
            raise HTTPException(500,detail="Internal Server Error")
        return {"new_token" : new_token}
    