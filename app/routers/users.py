# Protected routes: you need a valid token (and sometimes the admin role).

from typing import List

from fastapi import APIRouter, Depends

from app.db.database import get_all_users
from app.dependencies.auth import get_current_user, get_admin_user
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(tags=["Protected"])


# Any logged-in user
@router.get("/me", response_model=UserOut)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user


# Any logged-in user
@router.get("/protected-data")
async def protected_data(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, this is protected data!"}


# Admin only
@router.get("/admin/users", response_model=List[UserOut])
async def list_all_users(admin: User = Depends(get_admin_user)):
    return get_all_users()