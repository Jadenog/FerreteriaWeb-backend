from pydantic import BaseModel

class User(BaseModel):
    id : str | None = None
    name : str
    email :str
    es_admin : bool = False
    password : str
