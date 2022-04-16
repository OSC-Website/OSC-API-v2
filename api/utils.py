import os
from typing import Optional
from contextlib import asynccontextmanager

import asyncpg

import dotenv

dotenv.load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

@asynccontextmanager
async def asyncpg_connect(database_url: Optional[str] = None):
    """
    Custom context manager to use asyncpg

    Parameters
    ----------
        database_url (str, Optional): If not provided it will use the DATABASE_URL as the link

    Returns
    -------
        asyncpg.connection.Connection: The connection to the database
    """
    if database_url is None:
        connection = await asyncpg.connect(DATABASE_URL)
    else:
        connection = await asyncpg.connect(database_url)

    yield connection

    await connection.close()
