from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.database import Base

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    laid = Column(String, nullable=False)
    institution_id = Column(Integer, nullable=False)

# Enrollment moved to app.models.enrollment to avoid duplicate table definitions

class Grade(Base):
    __tablename__ = "grade"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    laid = Column(String, nullable=False)
    grade = Column(Float)
    institution_id = Column(Integer, nullable=False)