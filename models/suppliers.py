from config.database import Base
from sqlalchemy import Column,String,Integer

class Supplier(Base):
    __tablename__ = "suppliers"
    suid = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable=False)
    contact = Column(String,nullable=False)

def get_supplier(db,name):
    if name:
        supplier = db.query(Supplier).filter(Supplier.name == name).first()
        return supplier
    suppliers = db.query(Supplier).all()
    return suppliers

def add_supplier(db,name,phno):
    supplier = Supplier(
        name = name,
        contact = phno
    )
    db.add(supplier)
    db.flush()
    return supplier

def remove_supplier(db,suid):
    supplier = db.query(Supplier).filter(Supplier.suid == suid).first()
    db.delete(supplier)
    db.flush()
    return supplier
