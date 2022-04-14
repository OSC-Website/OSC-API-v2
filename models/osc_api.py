""" (module) osc_api
This contains the OSC_API (FastAPI subclass)
"""

import os
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import dotenv
import asyncpg


class OSC_API(FastAPI):
    """
    The custom subclas of FastAPI called OSC_API
    """

    def __init__(self) -> None:
        # Docs config
        self.title = "OSC-API-v2"
        self.description = "### This is an API to store users"
        self.license_info = {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        }

        # Rate limiting
        self.state.limiter = Limiter(key_func=get_remote_address)
        self.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

        # Database
        dotenv.load_dotenv()
        self.DATABASE_URL = os.environ["DATABASE_URL"]

    @asynccontextmanager
    async def asyncpg_connect(self, database_url: Optional[str] = None):
        """
        Custom context manager to use asyncpg

        Parameters
        ----------
            database_url (str, Optional): If not provided it will use the self.DATABASE_URL as the link

        Returns
        -------
            asyncpg.connection.Connection
        """
        if database_url is None:
            connection = await asyncpg.connect(self.DATABASE_URL)
        else:
            connection = await asyncpg.connect(database_url)

        yield connection

        await connection.close()
