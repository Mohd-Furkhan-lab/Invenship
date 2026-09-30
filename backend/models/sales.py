from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from models import Sales, Products
from config.database import Base


class Sales(Base):
    __tablename__ = "sales"
    sid = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, ForeignKey("products.pid"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)   
    total = Column(Float, nullable=False)
    date = Column(DateTime, server_default=func.now(), index=True)




def get_sales(db, skip: int = 0, limit: int = 50):
    rows = (
        db.query(
            Sales.sid,
            Sales.pid,
            Products.pname,
            Products.size,
            Sales.quantity,
            Sales.price,
            Sales.total,
            Sales.date,
        )
        .join(Products, Products.pid == Sales.pid)
        .order_by(Sales.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {
            "sid": r.sid,
            "pid": r.pid,
            "pname": r.pname,
            "size": r.size,
            "quantity": r.quantity,
            "price": r.price,
            "total": r.total,
            "date": r.date,
        }
        for r in rows
    ]

def add_sales(db,pid,quantity,price):
    sales = Sales(
        pid = pid,
        quantity = quantity,
        price = price,
        total = quantity*price
        )
    db.add(sales)
    db.flush()
    return sales

def delete_sales(db):
    sales = db.query(Sales).all()
    for s in sales:
        db.delete(s)
    db.flush()
    return sales