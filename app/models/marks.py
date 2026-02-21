from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    course_code = Column(String, nullable=False)
    marks = Column(Float, nullable=False)
    date = Column(Date, nullable=True)