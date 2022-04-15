# Standard library imports
import os

# Third party imports
from fastapi import Depends, APIRouter, HTTPException
from dotenv import load_dotenv
import asyncpg

# Local imports
from ..auth.classes import User
from ..auth.authenticate import get_current_active_user

load_dotenv()
db_url = os.environ["DATABASE_URL"]

users = APIRouter()

@users.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get basic info on your account
    """
    conn = await asyncpg.connect(db_url)
    db_result = await conn.fetch("SELECT * FROM USERS WHERE username=$1", current_user.username)
    await conn.close()
    return {
        "authentication_details" : current_user,
        "full_user" : db_result
    }