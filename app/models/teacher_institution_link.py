from sqlalchemy import Column, Integer, String
from app.database import Base

class TeacherInstitutionLink(Base):
    __tablename__ = "teacher_institution_link"

    id = Column(Integer, primary_key=True, index=True)
    teacher_x_session_code = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)
    role = Column(String, default="teacher")