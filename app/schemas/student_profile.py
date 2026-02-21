from pydantic import BaseModel

class StudentProfileCreate(BaseModel):
    laid: str
    institution_id: int
    name: str
    branch: str
    mobile: str
    email: str
    gender: str
    from pydantic import BaseModel
from typing import Optional

class StudentProfileCreate(BaseModel):
    laid: str
    institution_id: int
    name: str
    branch: str
    mobile: str
    email: str
    gender: str

class StudentProfileUpdate(BaseModel):
    laid: str
    institution_id: int
    name: Optional[str] = None
    branch: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None