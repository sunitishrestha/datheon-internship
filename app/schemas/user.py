# SCHEMA = the data we RECEIVE from or SEND to the user (checked by Pydantic).
# Notice: UserOut has NO password. We never send passwords back!

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, examples=["sunita"])
    password: str = Field(..., min_length=6, max_length=50, examples=["mypassword123"])


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # lets Pydantic read our User model

    username: str
    role: str