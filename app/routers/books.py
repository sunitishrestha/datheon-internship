# All the book URLs (CRUD = Create, Read, Update, Delete).

from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from app.db import database
from app.schemas.book import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


def get_book_or_404(book_id: int):
    """Find the book, or stop with a 404 error."""
    book = database.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found",
        )
    return book


# CREATE
@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED,
             summary="Create a new book")
async def create_book(book: BookCreate):
    return database.add_book(book.model_dump())


# READ ALL (with optional filters: /books?genre=Fantasy&author=Tolkien)
@router.get("", response_model=List[BookResponse], summary="Get all books")
async def get_books(genre: Optional[str] = None, author: Optional[str] = None):
    books = database.get_all_books()

    if genre:
        books = [b for b in books if b.genre.lower() == genre.lower()]
    if author:
        books = [b for b in books if author.lower() in b.author.lower()]

    return books


# READ ONE
@router.get("/{book_id}", response_model=BookResponse, summary="Get one book by ID")
async def get_book(book_id: int):
    return get_book_or_404(book_id)


# UPDATE
@router.put("/{book_id}", response_model=BookResponse, summary="Update a book")
async def update_book(book_id: int, book: BookCreate):
    get_book_or_404(book_id)
    return database.replace_book(book_id, book.model_dump())


# DELETE
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete a book")
async def delete_book(book_id: int):
    get_book_or_404(book_id)
    database.remove_book(book_id)