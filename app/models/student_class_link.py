from sqlalchemy import Column, Integer, String
from app.database import Base

class StudentClassLink(Base):
    __tablename__ = "student_class_link"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    class_id = Column(String, index=True, nullable=False)   # ex: "CSE-2A"