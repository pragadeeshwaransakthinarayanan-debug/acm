from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app.models.attendance import Attendance
from app.models.fees import Fees
from app.models.marks import Marks
from app.models.teacher_global import TeacherGlobal
from app.models.teacher_institution_link import TeacherInstitutionLink

router = APIRouter(prefix="/teacher", tags=["Teacher Portal"])

def verify_teacher(db: Session, teacher_laid: str, institution_id: int):
    t = db.query(TeacherGlobal).filter(TeacherGlobal.laid == teacher_laid).first()
    if not t:
        raise HTTPException(status_code=401, detail="Invalid teacher LAID")

    link = db.query(TeacherInstitutionLink).filter(
        TeacherInstitutionLink.teacher_laid == teacher_laid,
        TeacherInstitutionLink.institution_id == institution_id
    ).first()
    if not link:
        raise HTTPException(status_code=403, detail="Teacher not linked to this institution")

@router.get("/student/{student_laid}/attendance")
def get_student_attendance(
    student_laid: str,
    teacher_laid: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db)
):
    verify_teacher(db, teacher_laid, institution_id)
    rows = db.query(Attendance).filter(
        Attendance.laid == student_laid,
        Attendance.institution_id == institution_id
    ).all()
    return {"student_laid": student_laid, "attendance": rows}

@router.get("/student/{student_laid}/fees")
def get_student_fees(
    student_laid: str,
    teacher_laid: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db)
):
    verify_teacher(db, teacher_laid, institution_id)
    rows = db.query(Fees).filter(
        Fees.laid == student_laid,
        Fees.institution_id == institution_id
    ).all()
    return {"student_laid": student_laid, "fees": rows}

@router.get("/student/{student_laid}/marks")
def get_student_marks(
    student_laid: str,
    teacher_laid: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db)
):
    verify_teacher(db, teacher_laid, institution_id)
    rows = db.query(Marks).filter(
        Marks.laid == student_laid,
        Marks.institution_id == institution_id
    ).all()
    return {"student_laid": student_laid, "marks": rows}

