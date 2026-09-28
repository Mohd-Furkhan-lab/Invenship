from pydantic import BaseModel

class AddSales(BaseModel):
    name : str
    size : str
    quantity : int
    price : float
