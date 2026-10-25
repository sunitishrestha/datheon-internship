# SCHEMA = the data we RECEIVE and SEND. Pydantic checks it automatically.

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, examples=["The Hobbit"])
    author: str = Field(..., min_length=1, max_length=50, examples=["J.R.R. Tolkien"])
    publication_year: int = Field(..., gt=0, le=2026, examples=[1937])
    genre: str = Field(..., min_length=2, max_length=30, examples=["Fantasy"])
    price: float = Field(..., gt=0, examples=[14.99])


class BookResponse(BookCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int  # the response also includes the id