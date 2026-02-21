from sqlalchemy import Column, Integer, String
from app.database import Base

class StudentGlobal(Base):
    __tablename__ = "students_global"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)