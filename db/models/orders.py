from datetime import datetime
from pydantic import BaseModel, Field

class Order(BaseModel):
    id: str | None = None
    id_user: str
    id_product: str
    date: datetime = Field(default_factory=datetime.now) 
    total: float

    