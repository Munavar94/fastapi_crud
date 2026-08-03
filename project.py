from fastapi import FastAPI, Depends
from database import engine, get_db
from sqlalchemy.orm import Session
# from model import Book
import model
from pydantic import BaseModel, Field
from typing import Optional

# initialize the FastAPI app
app = FastAPI()

# 1. Create a Pydantic model for the request body
class Bookstore(BaseModel):
    id: Optional[int] = Field(None, title="ID of the book", description="The unique identifier of the book")
    title: str = Field(..., title="Title of the book", description="The title of the book")
    author: str = Field(..., title="Author of the book", description="The author of the book")
    publish_date: str = Field(..., title="Publish date of the book", description="The date when the book was published")

# 2.
@app.post("/books")
def create_book(book: Bookstore, db: Session = Depends(get_db)):
    # Create a new Book instance using the data from the request body
    new_book = model.Book(
        # id=len(db.query(model.Book).all()) + 1,  # Assign a new ID based on the current number of books in the database
        title=book.title,
        author=book.author,
        publish_date=book.publish_date
    )
    
    # Add the new book to the session and commit it to the database
    db.add(new_book)
    db.commit()
    db.refresh(new_book)  # Refresh the instance to get the updated data from the database
    
    return {"message": "Book created successfully", "book": new_book}

# 3. 
@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    # Query all books from the database
    books = db.query(model.Book).all()
    return books

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, title="Book Title", description="The title of the book")
    author: Optional[str] = Field(None, title="Book Author", description="The author of the book")
    publish_date: Optional[str] = Field(None, title="Publish Date", description="The date the book was published")

# 4. PUT | PATCH request to update a book
@app.patch("/books/{id}")
def update_book(id: int, book: BookUpdate, db: Session = Depends(get_db)):
    # Query the book by ID
    # existing_book = db.query(model.Book).filter(model.Book.id == id).first()
    existing_book = db.query(model.Book).filter(id == model.Book.id).first()
    
    if not existing_book:
        return {"message": "Book not found"}
    
    # Update the fields if they are provided in the request body
    if book.title is not None:
        existing_book.title = book.title
    if book.author is not None:
        existing_book.author = book.author
    if book.publish_date is not None:
        existing_book.publish_date = book.publish_date
    
    # Commit the changes to the database
    db.commit()
    db.refresh(existing_book)  # Refresh the instance to get the updated data from the database
    
    return {"message": "Book updated successfully", "book": existing_book}

# 5. DELETE request to delete a book
@app.delete("/books/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    # Query the book by ID
    existing_book = db.query(model.Book).filter(model.Book.id == id).first()

    if not existing_book:
        return {"message": "Book not found"}

    # Delete the book from the database
    db.delete(existing_book)
    db.commit()
    # db.refresh(existing_book)  # No need to Refresh the instance to get data from the database

    return {"message": "Book deleted successfully", "book": existing_book}