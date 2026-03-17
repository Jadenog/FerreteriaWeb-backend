import datetime

from pydantic import BaseModel

class New(BaseModel):
    id : str | None = None
    title : str
    description : str | None = None
    image : str 
    active : bool = True
    date : datetime = datetime.now()