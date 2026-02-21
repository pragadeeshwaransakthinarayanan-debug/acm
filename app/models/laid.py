from sqlalchemy import Column, Integer, String
from app.database import Base

class StudentGlobal(Base):
    __tablename__ = "students_global"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)