from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base

class Fees(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    laid = Column(String, index=True, nullable=False)
    institution_id = Column(Integer, index=True, nullable=False)

    amount = Column(Float, nullable=False)
    paid = Column(Integer, default=0)   # 0/1
    date = Column(Date, nullable=True)