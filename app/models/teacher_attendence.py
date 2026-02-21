from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class TeacherAttendance(Base):
    __tablename__ = "teacher_attendance"

    id = Column(Integer, primary_key=True, index=True)
    teacher_laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    date = Column(Date, nullable=True)
    status = Column(String, default="P")  # P/A/CL