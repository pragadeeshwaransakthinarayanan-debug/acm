from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.core.session_deps import get_current_student
from app.models.attendance import Attendance
from app.models.fees import Fee
from app.models.marks import Mark
from app.models.enrollment import Enrollment

router = APIRouter(prefix="/student", tags=["Student Portal"])


@router.get("/me/attendance")
def my_attendance(current=Depends(get_current_student), db: Session = Depends(get_db)):
    laid = current["laid"]
    institution_id = current["institution_id"]

    rows = db.query(Attendance).filter(
        Attendance.laid == laid,
        Attendance.institution_id == institution_id
    ).all()

    return {"attendance": rows}


@router.get("/me/marks")
def my_marks(current=Depends(get_current_student), db: Session = Depends(get_db)):
    laid = current["laid"]
    institution_id = current["institution_id"]

    rows = db.query(Mark).filter(
        Mark.laid == laid,
        Mark.institution_id == institution_id
    ).all()

    return {"marks": rows}


@router.get("/me/fees")
def my_fees(current=Depends(get_current_student), db: Session = Depends(get_db)):
    laid = current["laid"]
    institution_id = current["institution_id"]

    rows = db.query(Fee).filter(
        Fee.laid == laid,
        Fee.institution_id == institution_id
    ).all()

    return {"fees": rows}


@router.get("/me/courses")
def my_courses(current=Depends(get_current_student), db: Session = Depends(get_db)):
    laid = current["laid"]
    institution_id = current["institution_id"]

    rows = db.query(Enrollment).filter(
        Enrollment.laid == laid,
        Enrollment.institution_id == institution_id,
        Enrollment.status == "active"
    ).all()

    return {"courses": rows}