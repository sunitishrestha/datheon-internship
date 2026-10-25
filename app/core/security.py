# Everything about passwords and tokens lives here.

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES

# Tool that hashes and checks passwords using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Turn 'mypassword' into a scrambled hash we can safely store."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if the typed password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str) -> str:
    """Make a signed JWT token holding the username and an expiry time."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}  # "sub" = who the token is for
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)