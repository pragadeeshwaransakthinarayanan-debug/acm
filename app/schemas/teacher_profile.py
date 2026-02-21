from pydantic import BaseModel
from typing import Optional

class TeacherProfileCreate(BaseModel):
    x_session_code: str
    institution_id: int
    name: str
    qualification: str
    age: int
    mobile: str
    email: str
    gender: str

class TeacherProfileUpdate(BaseModel):
    name: Optional[str] = None
    qualification: Optional[str] = None
    age: Optional[int] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None