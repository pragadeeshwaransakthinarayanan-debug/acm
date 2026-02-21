from pydantic import BaseModel

class CourseCreate(BaseModel):
    name: str
    code: str

class CourseOut(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True