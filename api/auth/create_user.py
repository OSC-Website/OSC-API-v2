import os
import random
import asyncio

import asyncpg

from ..utils import asyncpg_connect
from .encryption import encrypt_text


db_url = os.environ["DATABASE_URL"]


async def create_database() -> None:
    conn = await asyncpg.connect(db_url)
    await conn.execute(
        """CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        year_level INTEGER NOT NULL,

        disabled INTEGER,
        username TEXT,
        password TEXT
        )"""
    )
    await conn.close()


async def create_super_user(
        first_name: str,
        last_name: str,
        email: str,
        disabled: int,
        year_level: int,
        username: str,
        password: str,
    ) -> None:

    hashed_password = await encrypt_text(password)

    async with asyncpg_connect(db_url) as conn:
        user_id = None
        while True:
            user_id = random.randint(1, 1000000000)
            data = await conn.fetch("SELECT * FROM Users WHERE user_id=$1", user_id)
            if len(data) == 0:
                break

        if user_id is None:
            return print("Error")
            
        await conn.execute(
            """INSERT INTO Users (
            user_id, first_name, last_name, email, disabled, year_level, username, password
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8
            )""",
            user_id,
            first_name,
            last_name,
            email,
            disabled,
            year_level,
            username,
            hashed_password,
        )


async def create_user(
        first_name: str,
        last_name: str,
        email: str,
        year_level: int,
    ) -> None:

    async with asyncpg_connect(db_url) as conn:

        user_id = None
        while True:
            user_id = random.randint(1, 1000000000)
            data = await conn.fetch("SELECT * FROM Users WHERE user_id=$1", user_id)
            if len(data) == 0:
                break

        if user_id is None:
            return print("Error")
        await conn.execute(
            """INSERT INTO Users (
            user_id, first_name, last_name, email, year_level
            ) VALUES (
                $1, $2, $3, $4, $5
            )""",
            user_id,
            first_name,
            last_name,
            email,
            year_level,
        )


if __name__ == "__main__":
    asyncio.run(create_database())

    # asyncio.run(
    #     create_super_user(
    #         first_name="",
    #         last_name="",
    #         email="",
    #         disabled=0,
    #         year_level=0,
    #         username="",
    #         password="",
    #     )
    # )
