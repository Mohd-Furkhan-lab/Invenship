from fastapi import HTTPException
from jwt import encode,decode,ExpiredSignatureError,InvalidTokenError
from datetime import datetime,timedelta,UTC
from dotenv import load_dotenv
import os
import uuid

def create_access_token(uid,role):
    payload = {
        "userid" : uid,
        "role" : role,
        "exp" : datetime.now(UTC)+timedelta(minutes=15),
        "type" : "access",
        "jti" : str(uuid.uuid4())
    }
    token = encode(payload,key=os.getenv("SECRET_KEY"),algorithm="HS256")
    return token


def create_refresh_token(uid,role):
    payload = {
        "userid" : uid,
        "role" : role,
        "exp" : datetime.now(UTC)+timedelta(days=7),
        "type" : "refresh",
        "jti" : str(uuid.uuid4())
    }
    token = encode(payload,key=os.getenv("SECRET_KEY"),algorithm="HS256")
    return token

def verify_token(token):
    try:
        payload = decode(token,key=os.getenv("SECRET_KEY"),algorithms=["HS256"])
    except InvalidTokenError:
        raise HTTPException(401,detail="Invalid Token")
    except ExpiredSignatureError:
        raise HTTPException(401,detail="Expired Token")
    return payload