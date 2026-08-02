from fastapi import FastAPI
from typing import Optional
from schemas.student import Student

# Initialize the FastAPI app
app = FastAPI()

@app.get("/")
async def root_home():
    return {"message": "Hello, Munavar!"}

@app.get("/greet")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}
# greet("Malik")    # wont work because it is not an async function and it is not called in the right way.
# it can work only http://127.0.0.1:8000/docs

# path parameter
@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}

# query parameter
@app.get("/greet_query")
async def greet_query(name: str = "World", age: Optional[int] = None):
    return {"message": f"Hello, {name}! You are {age} years old."}
# http://127.0.0.1:8000/greet_query?name=Munavar&age=32

# POST request with Pydantic model
@app.post("/create_student")
async def create_student(student: Student):
    return {"message": f"Student {student.name} created successfully!", "student": student}
    # return {
    #     "message": f"Student {student.name} created successfully!",
    #     "name": student.name,
    #     "age": student.age,
    #     "roll": student.roll
    # }

@app.get("/students/{roll}")
async def get_student(roll: int):
    # In a real application, you would fetch the student from a database
    # Here, we are just returning a dummy student for demonstration purposes
    dummy_student = Student(name="John Doe", age=20, roll=roll)
    return {"student": dummy_student}