from jwt import encode,decode
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
import uuid

def create_access_token(uid,role):
    payload = {
        "userid" : uid,
        "role" : role,
        "exp" : datetime+timedelta(min=15),
        "type" : "access",
        "jti" : uuid.uuid4()
    }
    token = encode(payload,key=os.getenv("SECRET_KEY"),algorithm="SHA256")
    return token


def create_refresh_token(uid,role):
    payload = {
        "userid" : uid,
        "role" : role,
        "exp" : datetime+timedelta(days=7),
        "type" : "refresh",
        "jti" : uuid.uuid4()
    }
    token = encode(payload,key=os.getenv("SECRET_KEY"),algorithm="SHA256")
    return token

