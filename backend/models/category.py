from sqlalchemy import Column,String,Integer
from backend.config.database import Base

class Category(Base):
    __tablename__ = "category"
    cid = Column(Integer,primary_key=True,autoincrement=True)
    cname = Column(String,nullable=False,unique=True)

def get_category(db,cname):
    category = db.query(Category).filter(Category.cname == cname.lower()).first()
    return category

def get_all_categories(db):
    categories = db.query(Category).all()
    return categories

def add_category(db,cname):
    category = Category(cname = cname.lower())
    db.add(category)
    db.flush()
    return category

def delete_category(db,cid):
    category = db.query(Category).filter(Category.cid == cid).first()
    db.delete(category)
    db.flush()
    return category
