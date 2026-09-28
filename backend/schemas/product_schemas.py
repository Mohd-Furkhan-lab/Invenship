from pydantic import BaseModel
from typing import Optional

class AddProduct(BaseModel):
    name : str
    brand : str
    price  : float
    stock : int
    size : str
    url : str
    category : str

class UpdateProducts(BaseModel):
    stock : Optional[int] = None
    price : Optional[float] = None
