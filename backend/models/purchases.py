from config.database import Base
from sqlalchemy import Column,Integer,Float,DateTime,ForeignKey
from datetime import date,UTC


class Purchase(Base):
    __tablename__ = "purchase"
    puid = Column(Integer,primary_key=True,autoincrement=True)
    pid =Column(Integer,ForeignKey("products.pid",ondelete="CASCADE"))
    quantity = Column(Integer,nullable=False)
    price = Column(Float,nullable=False)
    supplier = Column(Integer,ForeignKey("suppliers.suid",ondelete="CASCADE"))
    date = Column(DateTime,default=date.today())


def get_purchases(db):
    purchases = db.query(Purchase).all()
    return {"purchases" : purchases}

def add_purchase(db,pid,quantity,price,supplier,):
    purchse = Purchase(
        pid = pid,
        quantity = quantity,
        price = price,
        supplier = supplier
    )
    db.add(purchse)
    db.flush()
    return purchse

def delete_purchase(db):
    purchses = db.query(Purchase).all()
    for p in purchses:
        db.delete(p)
    db.flush()
    return purchses