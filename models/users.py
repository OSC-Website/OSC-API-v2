from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    year_level: int
    disabled: bool


@dataclass
class SuperUser(User):
    user_name: str
    hashed_password: str
