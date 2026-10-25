# MODEL = how a user looks INSIDE our database (includes the hashed password).

from dataclasses import dataclass


@dataclass
class User:
    username: str
    hashed_password: str
    role: str = "user"  # "user" or "admin"