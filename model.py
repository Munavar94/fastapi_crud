from sqlalchemy import Column, Integer, VARCHAR, Text, String, DateTime
from database import Base

# Book class - inherits from Base class
class Book(Base):
    # table name in the database created by this model
    __tablename__ = "books"

    # columns in the table
    id = Column(Integer, primary_key=True)  # index=True, autoincrement=True
    title = Column(VARCHAR(255), nullable=False)
    author = Column(Text, nullable=True)
    publish_date = Column(VARCHAR(255), nullable=False)
    # created_at = Column(DateTime, nullable=False)
