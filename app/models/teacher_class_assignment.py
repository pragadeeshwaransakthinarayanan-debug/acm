from sqlalchemy import Column, Integer, String
from app.database import Base

class TeacherClassAssignment(Base):
    __tablename__ = "teacher_class_assignment"

    id = Column(Integer, primary_key=True, index=True)
    teacher_laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    class_id = Column(String, index=True, nullable=False)   # ex: "CSE-2A"