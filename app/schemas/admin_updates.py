from pydantic import BaseModel
from datetime import date
from typing import Optional

class FeeUpsert(BaseModel):
    student_laid: str
    institution_id: int
    amount: float
    paid: int  # 0/1
    paid_on: Optional[date] = None

class SalaryUpsert(BaseModel):
    teacher_laid: str
    institution_id: int
    amount: float
    month: Optional[str] = None   # "2026-02"
    status: str = "paid"
    paid_on: Optional[date] = None