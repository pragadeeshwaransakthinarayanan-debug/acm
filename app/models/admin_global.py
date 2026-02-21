from sqlalchemy import Column, Integer, String
from app.database import Base

class AdminGlobal(Base):
    __tablename__ = "admins_global"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    email = Column(String)