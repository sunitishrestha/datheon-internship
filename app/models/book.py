# MODEL = how a book looks INSIDE our database.

from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    author: str
    publication_year: int
    genre: str
    price: float