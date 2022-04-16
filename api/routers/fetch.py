# Standard library imports
import os

# Third party imports
from fastapi import Depends, APIRouter, HTTPException
from dotenv import load_dotenv
import asyncpg

# Local imports
from ..auth.classes import User
from ..auth.authenticate import check_auth
from ..utils import asyncpg_connect

load_dotenv()
db_url = os.environ["DATABASE_URL"]

users = APIRouter()


@users.get("/api/users/me")  # for admin users to get their data
async def read_users_me(current_user: User = Depends(check_auth)):
    """
    Get basic info on your account
    """
    db_result = []
    async with asyncpg_connect(db_url) as conn:
        db_result = await conn.fetch(
            "SELECT * FROM USERS WHERE username=$1", current_user.username
        )

    response = {}

    for key, value in dict(db_result[0]).items():
        if key == "disabled":
            value = True if value == 1 else 0
        if value == None:
            continue
        response[key] = value

    return response


@users.get("/api/users/{user_id}")
async def find_by_id(user_id: int, current_user: User = Depends(check_auth)):
    """
    Find user by id
    """
    async with asyncpg_connect(db_url) as conn:
        db_result = await conn.fetch("SELECT * FROM USERS WHERE user_id=$1", user_id)

    if len(db_result) == 0:
        return HTTPException(404, "No user found")

    response = {}

    for key, value in dict(db_result[0]).items():
        if key == "disabled":
            value = True if value == 1 else 0
        if value == None:
            continue
        response[key] = value

    return {"user": response}


@users.get("/api/fetch/users/all")
async def get_all_users(current_user: User = Depends(check_auth)):
    response = []

    async with asyncpg_connect(db_url) as conn:
        db_result = await conn.fetch("SELECT * FROM USERS")

    for user in db_result:
        response_dict = {}
        for key, value in user.items():
            if key == "disabled":
                value = True if value == 1 else False
            if value == None:
                continue
            response_dict[key] = value

        response.append(response_dict)

    return {"user": response}


@users.get("/api/search_user/id")
async def search(
        user_id:int,
        amount: int = None,
        current_user: User = Depends(check_auth),
    ):
    async with asyncpg_connect(db_url) as conn:
        db_result = await conn.fetch("SELECT * FROM USERS WHERE user_id=$1", user_id)

    if len(db_result) == 0:
        return HTTPException(404, "No user found")

    response = {}
    for key, value in dict(db_result[0]).items():
        if key == "disabled":
            value = True if value == 1 else 0
        if value == None:
            continue
        response[key] = value

    return {"user": response}


@users.get("/api/search_user/firstname")
async def search(
        firstname:str,
        amount: int = None,
        current_user: User = Depends(check_auth),
    ):
    db_result = None
    async with asyncpg_connect(db_url) as conn:
        if amount is None:
            db_result = await conn.fetch("SELECT * FROM USERS WHERE first_name=$1", firstname)
        else:
            db_result = await conn.fetch("SELECT * FROM USERS WHERE first_name=$1 LIMIT $2", firstname, amount)

    if len(db_result) == 0 or db_result == None:
        return HTTPException(404, "No users found")

    response = []
    for user in db_result:
        response_dict = {}
        for key, value in dict(user).items():
            if key == "disabled":
                value = True if value == 1 else 0
            if value == None:
                continue
            response_dict[key] = value

        response.append(response_dict)

    return {"users": response}


@users.get("/api/search_user/lastname")
async def search(
        lastname:str,
        amount: int = None,
        current_user: User = Depends(check_auth),
    ):
    db_result = None
    async with asyncpg_connect(db_url) as conn:
        if amount is None:
            db_result = await conn.fetch("SELECT * FROM USERS WHERE last_name=$1", lastname)
        else:
            db_result = await conn.fetch("SELECT * FROM USERS WHERE last_name=$1 LIMIT $2", lastname, amount)

    if len(db_result) == 0 or db_result == None:
        return HTTPException(404, "No users found")

    response = []
    for user in db_result:
        response_dict = {}
        for key, value in dict(user).items():
            if key == "disabled":
                value = True if value == 1 else 0
            if value == None:
                continue
            response_dict[key] = value

        response.append(response_dict)

    return {"users": response}


@users.get("/api/search_user/year")
async def search(
        year:int,
        amount: int = None,
        current_user: User = Depends(check_auth),
    ):
    db_result = None
    async with asyncpg_connect(db_url) as conn:
        if amount is None:
            db_result = await conn.fetch("SELECT * FROM USERS WHERE year_level=$1", year)
        else:
            db_result = await conn.fetch("SELECT * FROM USERS WHERE year_level=$1 LIMIT $2", year, amount)

    if len(db_result) == 0 or db_result == None:
        return HTTPException(404, "No users found")

    response = []
    for user in db_result:
        response_dict = {}
        for key, value in dict(user).items():
            if key == "disabled":
                value = True if value == 1 else 0
            if value == None:
                continue
            response_dict[key] = value

        response.append(response_dict)

    return {"users": response}