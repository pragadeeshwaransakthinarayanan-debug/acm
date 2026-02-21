from pydantic import BaseModel
from datetime import date
from typing import Optional

class StudentFeeUpsert(BaseModel):
    student_x_session_code: str
    institution_id: int
    amount: float
    paid: int = 0
    date: Optional[date] = None

class TeacherSalaryUpsert(BaseModel):
    teacher_x_session_code: str
    institution_id: int
    amount: float
    month: str  # "2026-02"