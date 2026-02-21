from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.attendance import Attendance
from app.models.fees import Fees
from app.models.marks import Marks

router = APIRouter(prefix="/academic", tags=["Academic"])

@router.get("/{laid}")
def get_student_academic(laid: str, db: Session = Depends(get_db)):

    attendance = db.query(Attendance).filter(Attendance.laid == laid).all()
    fees = db.query(Fees).filter(Fees.laid == laid).all()
    marks = db.query(Marks).filter(Marks.laid == laid).all()

    return {
        "laid": laid,
        "attendance": attendance,
        "fees": fees,
        "marks": marks
    }