from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    """
    A base User - Used for authentication so its easier
    """
    username: str
    disabled: Optional[bool] = None
    

class UserInDB(User):
    """
    A subclass of `User` with the `hashed_password` attribute
    """
    hashed_password: str