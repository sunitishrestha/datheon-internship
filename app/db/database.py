# Our fake database (a dictionary) and simple functions to use it.
# Data is lost when the server restarts - fine for learning!

from typing import Optional, List

from app.models.book import Book

books_db: dict[int, Book] = {}
next_id = 1


def get_all_books() -> List[Book]:
    return list(books_db.values())


def get_book_by_id(book_id: int) -> Optional[Book]:
    return books_db.get(book_id)


def add_book(data: dict) -> Book:
    global next_id
    book = Book(id=next_id, **data)
    books_db[next_id] = book
    next_id += 1
    return book


def replace_book(book_id: int, data: dict) -> Book:
    book = Book(id=book_id, **data)
    books_db[book_id] = book
    return book


def remove_book(book_id: int) -> None:
    del books_db[book_id]