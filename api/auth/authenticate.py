# Standard library imports
from typing import Optional
import os

# Third party imports
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv

# Local imports
from .auth_db import get_user
from .encryption import encrypt_text, decrypt_token, encrypt_token
from .classes import User

load_dotenv()

oauth = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@oauth.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Token endpoint - Login here and get your token

    Username and Password are required and must be valid, if correct you will get your beautiful token

    Returns
    -------
        Dict[str, str]: The access token, token, and acess token type
    """
    user = await get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    hashed_password = await encrypt_text(form_data.password)

    if hashed_password != user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    key = os.environ["KEY"]
    token = await encrypt_token(key, user.username)

    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Decrypts a token to extract the user info from it, then it fetches the correct user from the db
    If user doesn't exist or invalid token it returns and raises an HTTPException

    Parameters
    ----------
        token (str): The users token

    Return
    ------
        User: The user or it returns none and raises an exception
    """
    key = os.environ["KEY"]
    decrypted_token = await decrypt_token(key, token)
    user = await get_user(decrypted_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def check_auth(current_user: User = Depends(get_current_user)) -> Optional[User]:
    """
    Check if user is active

    Returns
    -------
        If user is not disabled it returns the User
    """
    if current_user.disabled == True:
        raise HTTPException(status_code=400, detail="User is disabled")
    return current_user