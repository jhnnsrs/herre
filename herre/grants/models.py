from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str 
    first_name: Optional[str]
    last_name: Optional[str]