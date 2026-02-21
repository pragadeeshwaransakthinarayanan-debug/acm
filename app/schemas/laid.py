from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    laid: str
    full_name: str
    email: EmailStr

class StudentOut(StudentCreate):
    id: int

    class Config:
        orm_mode = True