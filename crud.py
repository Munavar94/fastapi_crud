from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from typing import Optional
from pydantic import BaseModel, Field

books = [
    {"id": 1, "title": "1984", "author": "George Orwell", 
     "publish_date": "1949-06-08"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "publish_date": "1960-07-11"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "publish_date": "1925-04-10"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "publish_date": "1813-01-28"},
]

# initialize the FastAPI app
app = FastAPI()

@app.get("/books")
async def get_books():
    return books        # getting all the books from the list

class Book(BaseModel):
    id: int = Field(..., title="Book ID", description="The unique identifier for the book")
    # id: Optional[int] = None  # Optional on input, generated on output
    title: str = Field(..., title="Book Title", description="The title of the book")
    author: Optional[str] = Field(None, title="Book Author", description="The author of the book")
    publish_date: Optional[str] = Field(None, title="Publish Date", description="The date the book was published")

@app.post('/books')
async def create_book(book: Book, status_code=status.HTTP_201_CREATED):
    # books.append(book.dict())
    new_book = book.model_dump()  # Convert Pydantic model to dictionary
    new_book["id"] = len(books) + 1  # Assign a new ID based on the current length of the books list
    # new_book["id"] = max((b["id"] for b in books), default=0) + 1
    books.append(new_book)
    return new_book         # appear only the book that is created, not all the books in the list.

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, title="Book Title", description="The title of the book")
    author: Optional[str] = Field(None, title="Book Author", description="The author of the book")
    publish_date: Optional[str] = Field(None, title="Publish Date", description="The date the book was published")

# PUT request to update a book
@app.put("/books/{book_id}")
async def update_book(book_id: int, book_update: BookUpdate):
    for book in books:
        if book["id"] == book_id:
            updated_book = book.copy()  # Create a copy of the existing book
            if book_update.title is not None:
                updated_book["title"] = book_update.title
            if book_update.author is not None:
                updated_book["author"] = book_update.author
            if book_update.publish_date is not None:
                updated_book["publish_date"] = book_update.publish_date
            books[books.index(book)] = updated_book  # Update the book in the list
            return updated_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# DELETE request to delete a book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")