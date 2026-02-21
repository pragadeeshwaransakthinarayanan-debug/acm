from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db

# Schemas
from app.schemas.teacher_profile import TeacherProfileCreate
from app.schemas.teacher_updates import StudentAttendanceUpsert, StudentMarksUpsert

# Models
from app.models.teacher_global import TeacherGlobal
from app.models.teacher_institution_link import TeacherInstitutionLink

from app.models.teacher_attendence import TeacherAttendance
from app.models.teacher_salary import TeacherSalary
from app.models.teacher_course_assignment import TeacherCourseAssignment

from app.models.attendance import Attendance
from app.models.marks import Marks  # if your class name is Marks (as your file says)


router = APIRouter(prefix="/teacher", tags=["Teacher Portal"])


# ==============================
# Helper: verify teacher
# ==============================
def verify_teacher(db: Session, teacher_laid: str, institution_id: int) -> TeacherGlobal:
    teacher = db.query(TeacherGlobal).filter(TeacherGlobal.laid == teacher_laid).first()
    if not teacher:
        raise HTTPException(status_code=401, detail="Invalid teacher LAID")

    link = db.query(TeacherInstitutionLink).filter(
        TeacherInstitutionLink.teacher_laid == teacher_laid,
        TeacherInstitutionLink.institution_id == institution_id
    ).first()
    if not link:
        raise HTTPException(status_code=403, detail="Teacher not linked to this institution")

    return teacher


# ==============================
# 1) Teacher profile CREATE (POST) - like student profile
# ==============================
@router.post("/profile")
def create_teacher_profile(
    payload: TeacherProfileCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(TeacherGlobal).filter(TeacherGlobal.laid == payload.laid).first()
    if existing:
        raise HTTPException(status_code=409, detail="Teacher profile already exists")

    teacher = TeacherGlobal(
        laid=payload.laid,
        name=payload.name,
        qualification=payload.qualification,
        age=payload.age,
        mobile=payload.mobile,
        email=payload.email,
        gender=payload.gender,
    )

    try:
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Teacher profile created", "id": teacher.id}


# ==============================
# 2) Teacher "me" (optional info) - returns only ids
# ==============================
@router.get("/me")
def teacher_me(
    teacher_laid: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    verify_teacher(db, teacher_laid, institution_id)
    return {"teacher_laid": teacher_laid, "institution_id": institution_id}


# ==============================
# 3) Teacher self endpoints
# ==============================
@router.get("/me/attendance")
def teacher_my_attendance(
    teacher_laid: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    verify_teacher(db, teacher_laid, institution_id)

    rows = db.query(TeacherAttendance).filter(
        TeacherAttendance.teacher_laid == teacher_laid,
        TeacherAttendance.institution_id == institution_id
    ).all()

    return rows


@router.get("/me/salary")
def teacher_my_salary(
    teacher_laid: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    verify_teacher(db, teacher_laid, institution_id)

    rows = db.query(TeacherSalary).filter(
        TeacherSalary.teacher_laid == teacher_laid,
        TeacherSalary.institution_id == institution_id
    ).all()

    return rows


@router.get("/me/courses")
def teacher_my_courses(
    teacher_laid: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    verify_teacher(db, teacher_laid, institution_id)

    rows = db.query(TeacherCourseAssignment).filter(
        TeacherCourseAssignment.teacher_laid == teacher_laid,
        TeacherCourseAssignment.institution_id == institution_id
    ).all()

    return rows


# ==============================
# 4) Teacher updates student attendance (UPSERT)
# ==============================
@router.post("/students/attendance")
def upsert_student_attendance(
    payload: StudentAttendanceUpsert,
    teacher_laid: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_teacher(db, teacher_laid, payload.institution_id)

    row = db.query(Attendance).filter(
        Attendance.laid == payload.student_laid,
        Attendance.institution_id == payload.institution_id,
        Attendance.course_code == payload.course_code,
        Attendance.date == payload.date
    ).first()

    if row:
        row.status = payload.status
    else:
        row = Attendance(
            laid=payload.student_laid,
            institution_id=payload.institution_id,
            course_code=payload.course_code,
            date=payload.date,
            status=payload.status
        )
        db.add(row)

    try:
        db.commit()
        db.refresh(row)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Attendance updated", "id": row.id}


# ==============================
# 5) Teacher updates student marks (UPSERT)
# ==============================
@router.post("/students/marks")
def upsert_student_marks(
    payload: StudentMarksUpsert,
    teacher_laid: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_teacher(db, teacher_laid, payload.institution_id)

    row = db.query(Marks).filter(
        Marks.laid == payload.student_laid,
        Marks.institution_id == payload.institution_id,
        Marks.course_code == payload.course_code,
        Marks.date == payload.date
    ).first()

    if row:
        row.marks = payload.marks
    else:
        row = Marks(
            laid=payload.student_laid,
            institution_id=payload.institution_id,
            course_code=payload.course_code,
            date=payload.date,
            marks=payload.marks
        )
        db.add(row)

    try:
        db.commit()
        db.refresh(row)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Marks updated", "id": row.id}