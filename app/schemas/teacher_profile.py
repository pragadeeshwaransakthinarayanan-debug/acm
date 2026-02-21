from pydantic import BaseModel

class TeacherProfileCreate(BaseModel):
    laid: str
    name: str
    qualification: str
    age: int
    mobile: str
    email: str
    gender: str