from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

# Initialize FastAPI App
app = FastAPI(
    title="BookStore REST API",
    description="An asynchronous CRUD REST API with auto-generated OpenAPI documentation and Pydantic validation.",
    version="1.0.0"
)

# ---------------------------------------------------------
# PYDANTIC SCHEMAS
# ---------------------------------------------------------

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="The title of the book", examples=["The Hobbit"])
    author: str = Field(..., min_length=1, max_length=50, description="The author of the book", examples=["J.R.R. Tolkien"])
    publication_year: int = Field(..., gt=0, le=2026, description="The year the book was published", examples=[1937])
    genre: str = Field(..., min_length=2, max_length=30, description="Genre of the book", examples=["Fantasy"])
    price: float = Field(..., gt=0.0, description="Price of the book", examples=[14.99])

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=50)
    publication_year: Optional[int] = Field(None, gt=0, le=2026)
    genre: Optional[str] = Field(None, min_length=2, max_length=30)
    price: Optional[float] = Field(None, gt=0.0)

class BookResponse(BookBase):
    id: int = Field(..., description="Unique database identifier for the book")

    class Config:
        from_attributes = True

# ---------------------------------------------------------
# IN-MEMORY DATA STORE (Simulating a Database)
# ---------------------------------------------------------
db_books = {}
id_counter = 1

# ---------------------------------------------------------
# API ENDPOINTS (CRUD)
# ---------------------------------------------------------

# 1. CREATE
@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED, summary="Create a new book")
async def create_book(book: BookCreate):
    global id_counter
    new_book = BookResponse(id=id_counter, **book.model_dump())
    db_books[id_counter] = new_book
    id_counter += 1
    return new_book

# 2. READ ALL (With Optional Query Filtering)
@app.get("/books", response_model=List[BookResponse], summary="Retrieve all books")
async def get_books(genre: Optional[str] = None, author: Optional[str] = None):
    books = list(db_books.values())
    
    if genre:
        books = [b for b in books if b.genre.lower() == genre.lower()]
    if author:
        books = [b for b in books if author.lower() in b.author.lower()]
        
    return books

# 3. READ ONE
@app.get("/books/{book_id}", response_model=BookResponse, summary="Get a specific book by ID")
async def get_book(book_id: int):
    if book_id not in db_books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with ID {book_id} not found"
        )
    return db_books[book_id]

# 4. UPDATE
@app.put("/books/{book_id}", response_model=BookResponse, summary="Update a book's details completely or partially")
async def update_book(book_id: int, book_update: BookUpdate):
    if book_id not in db_books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with ID {book_id} not found"
        )
    
    current_book_data = db_books[book_id].model_dump()
    update_data = book_update.model_dump(exclude_unset=True)
    
    # Merge current data with modifications
    updated_data = {**current_book_data, **update_data}
    
    db_books[book_id] = BookResponse(**updated_data)
    return db_books[book_id]

# 5. DELETE
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove a book from the catalog")
async def delete_book(book_id: int):
    if book_id not in db_books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Book with ID {book_id} not found"
        )
    del db_books[book_id]
    return None

# Run Server Locally
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port = 8000 ,reload= True)