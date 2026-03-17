from pydantic import BaseModel

class Product(BaseModel):
    id : str | None = None
    name : str
    description : str | None = None
    marca : str 
    price : float
    stock : int