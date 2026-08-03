from database import engine, Base
import model  # Import the model to ensure it's registered with Base

# Create all tables in the database of the Base class (which includes the Book model)
# from model import Book  # Import the Book model to ensure it's registered with Base
# 
Base.metadata.create_all(bind=engine)

# sqlalchemy (Base.metadata.create_all()) calls the create_all() method 
# on the Base class, which will create all tables defined in the models 
# that inherit from Base. In this case, it will create the "books" 
# table in the database specified in the .env file.