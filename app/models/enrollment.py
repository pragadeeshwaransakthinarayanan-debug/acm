from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    course_code = Column(String, nullable=False)
    enrolled_on = Column(Date, nullable=True)
    status = Column(String, default="active")