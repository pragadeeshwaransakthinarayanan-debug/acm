from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    x_session_code: str
    full_name: str
    email: EmailStr

class StudentOut(StudentCreate):
    id: int

    class Config:
        from_attributes = True