from pydantic import BaseModel
from typing import Optional

class AddProduct(BaseModel):
    name : str
    brand : str
    price  : float
    stock : int
    size : str
    url : str

class GetProducts(BaseModel):
    name : Optional[str] = None
    brand : Optional[str] = None
    size : Optional[str] = None

class UpdateProducts(BaseModel):
    stock : Optional[int] = None
    price : Optional[float] = None
