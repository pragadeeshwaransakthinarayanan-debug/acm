from sqlalchemy import Column, Integer, String
from app.database import Base

class TeacherGlobal(Base):
    __tablename__ = "teachers_global"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, unique=True, index=True, nullable=False)

    name = Column(String)
    qualification = Column(String)
    age = Column(Integer)
    mobile = Column(String)
    email = Column(String)
    gender = Column(String)