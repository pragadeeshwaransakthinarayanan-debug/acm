from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class TeacherSalary(Base):
    __tablename__ = "teacher_salary"

    id = Column(Integer, primary_key=True, index=True)
    teacher_laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    amount = Column(Float, nullable=False)
    month = Column(String, nullable=True)   # e.g. "2026-02"
    paid_on = Column(Date, nullable=True)
    status = Column(String, default="paid") # paid/pending