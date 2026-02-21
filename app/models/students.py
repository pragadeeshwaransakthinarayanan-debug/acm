from sqlalchemy import Column, Integer, String
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    email = Column(String, nullable=False)
    gender = Column(String, nullable=False)