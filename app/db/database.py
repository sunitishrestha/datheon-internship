# Our fake database (a dictionary) and simple functions to use it.
# Later (Task 3) you can replace this file with a real SQLite database.

from typing import Optional, List

from app.core.security import hash_password
from app.models.user import User

# username -> User object
users_db: dict[str, User] = {}


def get_user_by_username(username: str) -> Optional[User]:
    return users_db.get(username)


def get_all_users() -> List[User]:
    return list(users_db.values())


def create_user(username: str, password: str, role: str = "user") -> User:
    user = User(username=username, hashed_password=hash_password(password), role=role)
    users_db[username] = user
    return user


# Create one admin account so we can test roles
create_user("admin", "admin123", role="admin")