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
        sername (str) : The username to search for

    Returns:
        Union[bool, DBUser]
    """
    conn = await asyncpg.connect(DATABASE_URL)
    db_result = await conn.fetch("SELECT * FROM USERS WHERE username=$1", username)
    await conn.close()

    if not len(db_result):
        return False

    disabled = db_result[0][3]

    username = db_result[0][5]
    hashed_password = db_result[0][6]

    user = UserInDB(
        username=username, hashed_password=hashed_password, disabled=disabled
    )

    return user


# import asyncio
# if __name__ == "__main__":
#     asyncio.run(get_user("FusionSid"))
