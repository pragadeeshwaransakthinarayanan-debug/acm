from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app.models.students_global import StudentGlobal
from app.models.teacher_global import TeacherGlobal
from app.schemas.admin_updates import FeeUpsert, SalaryUpsert
from app.models.fees import Fees
from app.models.teacher_salary import TeacherSalary
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/admin", tags=["Admin Portal"])


def verify_admin(db: Session, laid: str):
    # For now just check LAID exists in teacher table
    admin = db.query(TeacherGlobal).filter(
        TeacherGlobal.laid == laid
    ).first()

    if not admin:
        raise HTTPException(status_code=401, detail="Invalid LAID")

    return admin


@router.get("/students")
def view_students(
    laid: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    verify_admin(db, laid)

    students = db.query(StudentGlobal).filter(
        StudentGlobal.institution_id == institution_id
    ).all()

    return students


@router.get("/teachers")
def view_teachers(
    laid: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    verify_admin(db, laid)

    teachers = db.query(TeacherGlobal).all()

    return teachers
@router.post("/fees")
def upsert_fee(
    payload: FeeUpsert,
    laid: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_admin(db, laid)  # your existing verify_admin

    row = db.query(Fees).filter(
        Fees.laid == payload.student_laid,
        Fees.institution_id == payload.institution_id,
        Fees.date == payload.date
    ).first()

    if row:
        row.amount = payload.amount
        row.paid = payload.paid
    else:
        row = Fees(
            laid=payload.student_laid,
            institution_id=payload.institution_id,
            amount=payload.amount,
            paid=payload.paid,
            date=payload.date
        )
        db.add(row)

    try:
        db.commit()
        db.refresh(row)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Fee updated", "id": row.id}


@router.post("/salary")
def upsert_salary(
    payload: SalaryUpsert,
    laid: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_admin(db, laid)

    row = db.query(TeacherSalary).filter(
        TeacherSalary.teacher_laid == payload.teacher_laid,
        TeacherSalary.institution_id == payload.institution_id,
        TeacherSalary.month == payload.month
    ).first()

    if row:
        row.amount = payload.amount
        row.status = payload.status
        row.paid_on = payload.paid_on
    else:
        row = TeacherSalary(
            teacher_laid=payload.teacher_laid,
            institution_id=payload.institution_id,
            amount=payload.amount,
            month=payload.month,
            status=payload.status,
            paid_on=payload.paid_on
        )
        db.add(row)

    try:
        db.commit()
        db.refresh(row)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Salary updated", "id": row.id}