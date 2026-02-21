from pydantic import BaseModel
from datetime import date

class StudentAttendanceUpsert(BaseModel):
    student_x_session_code: str
    institution_id: int
    course_code: str
    date: date
    status: str  # "present"/"absent"

class StudentMarksUpsert(BaseModel):
    student_x_session_code: str
    institution_id: int
    course_code: str
    date: date
    marks: float