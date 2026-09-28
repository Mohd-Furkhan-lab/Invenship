from pydantic import BaseModel

class AddSupplier(BaseModel):
    name : str
    phno : str