from fastapi import HTTPException
from backend.models.user import get_user,add_user,update_role,delete_user
from backend.config.database import SesssionLocal
from bcrypt import hashpw,gensalt

def getusers(is_admin,email):
    if is_admin:
        with SesssionLocal() as db:
            res = get_user(db,email)
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
            return {"data" : res}

def adduser(is_admin,data):
    if is_admin:
        with SesssionLocal() as db:
            user = get_user(db,data.email)
            if user:
                raise HTTPException(309,detail="User Already Exists")
            hash_pw = hashpw(data.password.encode('utf-8'),gensalt()).decode('utf-8')
            res = add_user(db,data.name,data.email,hash_pw,data.role)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
        return {"message" : f"{data.name} added succssfully"}

def updaterole(is_admin,data):
    if is_admin:
        with SesssionLocal() as db:
            user = get_user(db,data.email)
            if user is None:
                raise HTTPException(404,detail="User Not Found")
            res = update_role(db,data.email,data.new_role)
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
        return {"message" : f"{user.get("username")} updated to {data.new_role}"}

def deleteuser(is_admin,email):
    if is_admin:
        with SesssionLocal() as db:
            user = get_user(db,email)
            if user is None:
                raise HTTPException(404,detail="User Not Found")
            res = delete_user(db,user.get("uid"))
            db.commit()
            if res is None:
                raise HTTPException(500,detail="Internal Server Error")
        return {"message" : f"{user.get("username")} deleted successfully"}

