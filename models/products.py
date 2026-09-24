from sqlalchemy import Column,String,Integer,ForeignKey,Float
from config.database import Base

class Products(Base):
    __tablename__ = "products"
    pid = Column(Integer,primary_key=True,autoincrement=True)
    cid = Column(Integer,ForeignKey("category.cid",ondelete="CASCADE"),nullable=False)
    pname = Column(String,nullable=False,unique=True)
    pimage = Column(String,nullable=True)
    size = Column(String,nullable=False)
    brand = Column(String,nullable=False)
    price = Column(Float,nullable=False)
    stock = Column(Integer,nullable=False)

def get_products(db,pname=None, brand=None, size=None):
        query = db.query(Products)
        filters = []
        if pname:
            filters.append(Products.pname == pname)
        if brand:
            filters.append(Products.brand == brand)
        if size:
            filters.append(Products.size == size)
        if filters:
            query = query.filter(*filters)
        return query.all()

def add_product(db,cid,pname,url,size,brand,price,stock):
    product = Products(
        cid = cid,
        pname = pname,
        pimage = url,
        size = size,
        brand = brand,
        price = price,
        stock = stock
    ) 
    db.add(product)
    db.flush()
    return product

def update_product_details(db,pid,price=None,stock=None):
    product = db.query(Products).filter(Products.pid == pid).first()
    if price:
        product.price = price
    if stock:
        product.stock = stock
    db.flush()
    return product

def delete_product(db,pid):
    product = db.query(Products).filter(Products.pid == pid).first()
    db.delete(product)
    db.flush()
    return product

def update_stock(db,pid,new_count):
    product = db.query(Products).filter(Products.pid == pid).first()
    product.stock = new_count
    db.flush()
    return product