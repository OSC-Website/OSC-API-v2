import asyncio
import os
import asyncpg
from encryption import encrypt_text


db_url = os.environ["DATABASE_URL"]


async def create_database() -> None:
    conn = await asyncpg.connect(db_url)
    await conn.execute(
        """CREATE TABLE IF NOT EXISTS Users (
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        disabled INTEGER NOT NULL,
        year_level INTEGER NOT NULL,
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

    conn = await asyncpg.connect(db_url)
    await conn.execute(
        """INSERT INTO Users (
        first_name, last_name, email, disabled, year_level, username, password
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7
        )""",
        first_name,
        last_name,
        email,
        disabled,
        year_level,
        username,
        hashed_password,
    )
    await conn.close()


if __name__ == "__main__":
    # asyncio.run(create_database())

    asyncio.run(
        create_super_user(
            first_name="Siddhesh",
            last_name="Zantye",
            email="siddheshadsv@icloud.com",
            disabled=1,
            year_level=11,
            username="FusionSid",
            password="Password",
        )
    )
