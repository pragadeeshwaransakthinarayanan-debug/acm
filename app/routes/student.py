from sqlalchemy import Column, Integer, String
from app.database import Base
from fastapi import APIRouter

router = APIRouter(prefix="/students", tags=["Students"])


id = Column(Integer, primary_key=True, index=True)
name = Column(String, nullable=False)
email = Column(String, unique=True, index=True, nullable=False)
institution_id = Column(Integer, nullable=False)