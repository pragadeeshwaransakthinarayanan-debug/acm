from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db

from app.models.teacher_global import TeacherGlobal
from app.models.teacher_institution_link import TeacherInstitutionLink
from app.models.attendance import Attendance
from app.models.marks import Mark

from app.schemas.teacher_updates import StudentAttendanceUpsert, StudentMarksUpsert
from app.schemas.teacher_profile import TeacherProfileCreate, TeacherProfileUpdate

router = APIRouter(prefix="/teacher", tags=["Teacher Portal"])


def verify_teacher(db: Session, teacher_x_session_code: str, institution_id: int) -> TeacherGlobal:
    t = db.query(TeacherGlobal).filter(TeacherGlobal.x_session_code == teacher_x_session_code).first()
    if not t:
        raise HTTPException(status_code=401, detail="Invalid teacher x-session code")

    link = db.query(TeacherInstitutionLink).filter(
        TeacherInstitutionLink.teacher_x_session_code == teacher_x_session_code,
        TeacherInstitutionLink.institution_id == institution_id
    ).first()
    if not link:
        raise HTTPException(status_code=403, detail="Teacher not linked to this institution")

    return t


# ---------------------------
# Teacher profile (create/upsert + view)
# ---------------------------

@router.post("/profile")
def create_teacher_profile(payload: TeacherProfileCreate, db: Session = Depends(get_db)):
    existing = db.query(TeacherGlobal).filter(TeacherGlobal.x_session_code == payload.x_session_code).first()
    if existing:
        raise HTTPException(status_code=409, detail="Teacher already exists")

    t = TeacherGlobal(**payload.model_dump(exclude={"institution_id"}))
    db.add(t)

    # also create link
    link = TeacherInstitutionLink(teacher_x_session_code=payload.x_session_code, institution_id=payload.institution_id)
    db.add(link)

    try:
        db.commit()
        db.refresh(t)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Teacher created", "x_session_code": t.x_session_code}


@router.get("/profile")
def get_teacher_profile(
    teacher_x_session_code: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    t = verify_teacher(db, teacher_x_session_code, institution_id)
    return {
        "x_session_code": t.x_session_code,
        "name": t.name,
        "qualification": t.qualification,
        "age": t.age,
        "mobile": t.mobile,
        "email": t.email,
        "gender": t.gender,
    }


@router.put("/profile")
def update_teacher_profile(
    payload: TeacherProfileUpdate,
    teacher_x_session_code: str = Query(...),
    institution_id: int = Query(...),
    db: Session = Depends(get_db),
):
    t = verify_teacher(db, teacher_x_session_code, institution_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(t, field, value)

    db.commit()
    db.refresh(t)
    return {"message": "Teacher profile updated"}


# ---------------------------
# Teacher updates student data
# ---------------------------

@router.post("/students/attendance")
def upsert_student_attendance(
    payload: StudentAttendanceUpsert,
    teacher_x_session_code: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_teacher(db, teacher_x_session_code, payload.institution_id)

    row = db.query(Attendance).filter(
        Attendance.x_session_code == payload.student_x_session_code,
        Attendance.institution_id == payload.institution_id,
        Attendance.course_code == payload.course_code,
        Attendance.date == payload.date
    ).first()

    if row:
        row.status = payload.status
    else:
        row = Attendance(
            x_session_code=payload.student_x_session_code,
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

    return {"message": "Attendance upserted", "id": row.id}


@router.post("/students/marks")
def upsert_student_marks(
    payload: StudentMarksUpsert,
    teacher_x_session_code: str = Query(...),
    db: Session = Depends(get_db),
):
    verify_teacher(db, teacher_x_session_code, payload.institution_id)

    row = db.query(Mark).filter(
        Mark.x_session_code == payload.student_x_session_code,
        Mark.institution_id == payload.institution_id,
        Mark.course_code == payload.course_code,
        Mark.date == payload.date
    ).first()

    if row:
        row.marks = payload.marks
    else:
        row = Mark(
            x_session_code=payload.student_x_session_code,
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

    return {"message": "Marks upserted", "id": row.id}
from app.core.session_deps import get_current_teacher
from app.models.session import SessionToken
@router.get("/me/profile")
def get_my_profile(
    session: SessionToken = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    teacher_x_session_code = session.x_session_code
    institution_id = session.institution_id
    t = verify_teacher(db, teacher_x_session_code, institution_id)
    return {
        "x_session_code": t.x_session_code,
        "name": t.name,
        "qualification": t.qualification,
        "age": t.age,
        "mobile": t.mobile,
        "email": t.email,
        "gender": t.gender,
    }
@router.post("/me/students/attendance")
def upsert_attendance(
    payload: StudentAttendanceUpsert,
    session: SessionToken = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    teacher_x_session_code = session.x_session_code
    institution_id = session.institution_id

    if payload.institution_id != institution_id:
        raise HTTPException(status_code=403, detail="Institution mismatch")
    ...