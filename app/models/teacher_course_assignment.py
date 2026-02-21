from sqlalchemy import Column, Integer, String
from app.database import Base

class TeacherCourseAssignment(Base):
    __tablename__ = "teacher_course_assignment"

    id = Column(Integer, primary_key=True, index=True)
    teacher_laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)
    course_code = Column(String, index=True, nullable=False)  # ex: CS22403