from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db

from app.models.students import Student
from app.models.teacher_global import TeacherGlobal
from app.models.fees import Fee
from app.models.teacher_salary import TeacherSalary

from app.models.admin_global import AdminGlobal
from app.models.admin_institution_link import AdminInstitutionLink

from app.schemas.admin_updates import StudentFeeUpsert, TeacherSalaryUpsert

router = APIRouter(prefix="/admin", tags=["Admin Portal"])


def verify_admin(db: Session, admin_x_session_code: str, institution_id: int):
    a = db.query(AdminGlobal).filter(AdminGlobal.x_session_code == admin_x_session_code).first()
    if not a:
        raise HTTPException(status_code=401, detail="Invalid admin x-session code")

    link = db.query(AdminInstitutionLink).filter(
        AdminInstitutionLink.admin_x_session_code == admin_x_session_code,
        AdminInstitutionLink.institution_id == institution_id
    ).first()

    if not link:
        raise HTTPException(status_code=403, detail="Admin not linked to this institution")


@router.get("/students")
def view_students(
    admin_x_session_code: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    verify_admin(db, admin_x_session_code, institution_id)
    rows = db.query(Student).filter(Student.institution_id == institution_id).all()
    return rows


@router.get("/teachers")
def view_teachers(
    admin_x_session_code: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    verify_admin(db, admin_x_session_code, institution_id)
    # if TeacherGlobal does not have institution_id, you may need to join with TeacherInstitutionLink
    rows = db.query(TeacherGlobal).all()
    return rows


@router.post("/students/fees")
def upsert_student_fee(
    payload: StudentFeeUpsert,
    admin_x_session_code: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_admin(db, admin_x_session_code, payload.institution_id)

    row = Fee(
        x_session_code=payload.student_x_session_code,
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

    return {"message": "Fee record added", "id": row.id}


@router.post("/teachers/salary")
def upsert_teacher_salary(
    payload: TeacherSalaryUpsert,
    admin_x_session_code: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_admin(db, admin_x_session_code, payload.institution_id)

    row = TeacherSalary(
        teacher_x_session_code=payload.teacher_x_session_code,
        institution_id=payload.institution_id,
        amount=payload.amount,
        month=payload.month
    )
    db.add(row)

    try:
        db.commit()
        db.refresh(row)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Salary record added", "id": row.id}