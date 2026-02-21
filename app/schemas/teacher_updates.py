from pydantic import BaseModel
from datetime import date
from typing import Optional

class StudentAttendanceUpsert(BaseModel):
    student_laid: str
    institution_id: int
    course_code: str
    attendance_date: Optional[date] = None
    status: str  # "P" / "A"

class StudentMarksUpsert(BaseModel):
    student_laid: str
    institution_id: int
    course_code: str
    marks: float
    marks_date: Optional[date] = None