from config.database import Base
from sqlalchemy import Column,String,Integer

class User(Base):
    __tablename__ = "user"
    uid = Column(Integer,primary_key=True,autoincrement=True)
    username =  Column(String,default="user")
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    role = Column(String,default="user")


#User Queries
def get_details(db,uid):
    user = db.query(User.email,User.username).filter(User.uid == uid).first()
    return user._asdict()

def change_password(db,uid,new_password):
    user = db.query(User).filter(User.uid == uid).first()
    user.password = new_password
    db.flush()
    return user



#Admin Queries
def get_user(db,email=None,userid=None):
    if email :
        user =  db.query(User.uid,User.username,User.email,User.role,User.password).filter(User.email == email).first()
    if userid:
        user =  db.query(User.uid,User.username,User.email,User.role,User.password).filter(User.uid == userid).first()
    return user._asdict()

def add_user(db,username,email,password,role):
    user = User(
        username = username,
        email = email,
        password = password,
        role = role
    )
    db.add(user)
    db.flush()
    return user

def update_role(db,email,new_role):
    user = db.query(User).filter(User.email == email).first()
    user.role = new_role
    db.flush()
    return user

def delete_user(db,email):
    user = db.query(User).filter(User.email == email).first()
    db.delete(user)
    db.flush()
    return user