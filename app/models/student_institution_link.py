from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class StudentInstitutionLink(Base):
    __tablename__ = "student_institution_link"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, ForeignKey("students_global.laid"), nullable=False)
    institution_id = Column(Integer, nullable=False)
    status = Column(String, default="active")