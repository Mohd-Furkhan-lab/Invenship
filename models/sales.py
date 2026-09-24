from sqlalchemy import Column,String,Integer,Float,DateTime
from datetime import datetime,UTC
from config.database import Base

class Sales(Base):
    __tablename__ = "sales"
    sid = Column(Integer,primary_key=True,autoincrement=True)
    pname = Column(String,nullable=False)
    size = Column(String,nullable=False)
    quantity = Column(Integer,nullable=False)
    price = Column(Float,nullable=False)
    total = Column(Float,nullable=False)
    timestamp = Column(DateTime,default=datetime.now(UTC))

def get_sales(db):
    sales = db.query(Sales).all()
    return sales

def add_sales(db,name,size,quantity,price):
    sales = Sales(
        pname = name,
        size = size,
        quantity = quantity,
        price = price,
        total = quantity*price
        )
    db.add(sales)
    db.flush()
    return sales

def delete_sales(db):
    sales = db.query(Sales).all()
    db.delete(sales)
    db.flush()
    return sales