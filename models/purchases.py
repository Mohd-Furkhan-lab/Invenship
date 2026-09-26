from config.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey
from datetime import datetime,UTC

class Purchase(Base):
    __tablename__ = "purchase"
    puid = Column(Integer,primary_key=True,autoincrement=True)
    pname = Column(String,nullable=False)
    quantity = Column(Integer,nullable=False)
    price = Column(Float,nullable=False)
    supplier = Column(Integer,ForeignKey("supplier.suid",ondelete="CASCADE"))
    timestamp = Column(DateTime,default=datetime.now(UTC))


def get_purchases(db):
    purchases = db.query(Purchase).all()
    return {"purchases" : purchases}

def add_purchase(db,pname,quantity,price,supplier,):
    purchse = Purchase(
        pname = pname,
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