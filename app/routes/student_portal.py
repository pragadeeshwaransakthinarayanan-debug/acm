from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db

from app.models.attendance import Attendance
from app.models.fees import Fees
from app.models.marks import Marks
from app.models.enrollment import Enrollment
from app.models.students import Student
from app.schemas.student_profile import StudentProfileCreate

router = APIRouter(prefix="/student", tags=["Student Portal"])


@router.get("/{laid}/attendance")
def student_attendance(
    laid: str,
    institution_id: int = Query(...),
    db: Session = Depends(get_db)
):
    rows = db.query(Attendance).filter(
        Attendance.laid == laid,
        Attendance.institution_id == institution_id
    ).all()

    return {
        "laid": laid,
        "institution_id": institution_id,
        "attendance": [
            {"course_code": r.course_code, "status": r.status, "date": str(r.date) if r.date else None}
            for r in rows
        ]
    }


@router.get("/{laid}/fees")
def student_fees(
    laid: str,
    institution_id: int = Query(...),
    db: Session = Depends(get_db)
):
    rows = db.query(Fees).filter(
        Fees.laid == laid,
        Fees.institution_id == institution_id
    ).all()

    return {
        "laid": laid,
        "institution_id": institution_id,
        "fees": [
            {"amount": r.amount, "paid": r.paid, "date": str(r.date) if r.date else None}
            for r in rows
        ]
    }


@router.get("/{laid}/marks")
def student_marks(
    laid: str,
    institution_id: int = Query(...),
    db: Session = Depends(get_db)
):
    rows = db.query(Marks).filter(
        Marks.laid == laid,
        Marks.institution_id == institution_id
    ).all()

    return {
        "laid": laid,
        "institution_id": institution_id,
        "marks": [
            {"course_code": r.course_code, "marks": r.marks, "date": str(r.date) if r.date else None}
            for r in rows
        ]
    }


@router.get("/{laid}/courses")
def student_courses(
    laid: str,
    institution_id: int = Query(...),
    db: Session = Depends(get_db)
):
    rows = db.query(Enrollment).filter(
        Enrollment.laid == laid,
        Enrollment.institution_id == institution_id,
        Enrollment.status == "active"
    ).all()

    return {
        "laid": laid,
        "institution_id": institution_id,
        "courses": [
            {"course_code": r.course_code, "enrolled_on": str(r.enrolled_on) if r.enrolled_on else None}
            for r in rows
        ]
    }


@router.post("/profile")
def create_student_profile(
    payload: StudentProfileCreate,
    db: Session = Depends(get_db),
):
    # prevent duplicates (same laid + institution)
    existing = db.query(Student).filter(
        Student.laid == payload.laid,
        Student.institution_id == payload.institution_id
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Student profile already exists")

    student = Student(**payload.dict())

    try:
        db.add(student)
        db.commit()
        db.refresh(student)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Student profile created", "id": student.id}