from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta
from app.database import Base

class SessionToken(Base):
    __tablename__ = "session_tokens"

    id = Column(Integer, primary_key=True, index=True)

    # token stored in DB
    token = Column(String, unique=True, index=True, nullable=False)

    # who logged in
    role = Column(String, nullable=False)  # "student" | "teacher" | "admin"
    laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)