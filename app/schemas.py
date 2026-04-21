from pydantic import BaseModel, Field, conint

class UserIn(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    age: conint(ge=0, le=150) = Field(..., description="Age must be between 0 and 150")

class UserOut(BaseModel):
    id: int
    username: str
    age: int