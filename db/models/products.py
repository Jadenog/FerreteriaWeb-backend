from pydantic import BaseModel

class Product(BaseModel):
    id : str | None = None
    name : str
    description : str | None = None
    price : float
    stock : int