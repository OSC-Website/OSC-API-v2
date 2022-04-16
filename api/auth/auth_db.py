""" (module) auth_db
"""

# Standard library imports
import os
from typing import Union

# Third party imports
import asyncpg
from dotenv import load_dotenv

# Local imports-
from .classes import UserInDB

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]


async def get_user(username: str) -> Union[bool, UserInDB]:
    """
    Gets a specific user from the Users table if not found it will return False

    Parameters:
        username (str): The username to search for

    Returns:
        Union[bool, UserInDB]: If user is not found it returns false. else
    """
    conn = await asyncpg.connect(DATABASE_URL)
    db_result = await conn.fetch("SELECT * FROM USERS WHERE username=$1", username)
    await conn.close()

    if not len(db_result):
        return False

    disabled = True if db_result[0][5] == 0 else False
    username = db_result[0][6]
    hashed_password = db_result[0][7]

    user = UserInDB(
        username=username, hashed_password=hashed_password, disabled=disabled
    )

    return user


# test
# import asyncio
# if __name__ == "__main__":
#     asyncio.run(get_user("FusionSid")) 
