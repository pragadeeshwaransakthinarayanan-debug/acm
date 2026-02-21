from pydantic import BaseModel, EmailStr, ConfigDict

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    institution_id: int

class StudentOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    institution_id: int

    model_config = ConfigDict(from_attributes=True)