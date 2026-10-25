from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.config import SECRET_KEY,ALGORITHM 
from app.db.database import get_user_by_username
from app.models.user import User

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Read the token, check it, and return the logged-in user."""
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise error
    except JWTError:
        raise error

    user = get_user_by_username(username)
    if user is None:
        raise error
    return user


def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Only lets admins through (RBAC = Role Based Access Control)."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only!",
        )
    return current_user


   