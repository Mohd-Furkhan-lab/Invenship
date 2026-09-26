from pydantic import BaseModel

class AddPurchase(BaseModel):
    name : str
    size : str
    quantity : int
    price : float
    supplier : str