from pydantic import BaseModel

class AddPurchase(BaseModel):
    name : str
    quantity : int
    price : float
    supplier : str