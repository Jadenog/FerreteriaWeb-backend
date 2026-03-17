from datetime import datetime
from pydantic import BaseModel, Field

class New(BaseModel):
    id: str | None = None
    title: str
    description: str | None = None
    image: str
    active: bool = True
    date: datetime = Field(default_factory=datetime.now)