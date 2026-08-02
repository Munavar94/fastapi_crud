from pydantic import BaseModel, Field
from typing import Optional

class Student(BaseModel):
    name: str = Field(..., title="Student Name", description="The full name of the student")
    age: Optional[int] = Field(None, title="Student Age", description="The age of the student in years")
    # grade: str = Field(..., title="Student Grade", description="The current grade level of the student")
    # email: str = Field(..., title="Student Email", description="The email address of the student")
    roll: int = Field(..., title="Student Roll Number", description="The roll number assigned to the student")

# Response in JSON format:
# {
#     "name": "John Doe",
#     "age": 20,
#     "roll": 123
# }