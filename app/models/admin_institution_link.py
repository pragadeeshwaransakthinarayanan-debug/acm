from sqlalchemy import Column, Integer, String
from app.database import Base

class AdminInstitutionLink(Base):
    __tablename__ = "admin_institution_link"

    id = Column(Integer, primary_key=True, index=True)
    admin_x_session_code = Column(String, index=True)
    institution_id = Column(Integer, index=True)