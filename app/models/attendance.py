from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    date = Column(Date, nullable=True)
    course_code = Column(String, nullable=True)
    status = Column(String, nullable=False, default="P")