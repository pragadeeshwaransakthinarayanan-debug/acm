import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session import SessionToken

# change these model imports based on your project
from app.models.students import Student
from app.models.teacher_global import TeacherGlobal
from app.models.admin_global import AdminGlobal

router = APIRouter(prefix="/auth", tags=["Auth (Session)"])


@router.post("/login")
def login(role: str, laid: str, password: str, institution_id: int, db: Session = Depends(get_db)):
    role = role.lower()

    if role == "student":
        user = db.query(Student).filter(Student.laid == laid, Student.institution_id == institution_id).first()
    elif role == "teacher":
        user = db.query(TeacherGlobal).filter(TeacherGlobal.laid == laid).first()
    elif role == "admin":
        user = db.query(AdminGlobal).filter(AdminGlobal.laid == laid).first()
    else:
        raise HTTPException(status_code=400, detail="Invalid role")

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # If you store password in DB (example: user.password)
    if getattr(user, "password", None) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # create session token
    token = secrets.token_urlsafe(32)

    db.add(SessionToken(
        token=token,
        laid=laid,
        institution_id=institution_id,
        role=role
    ))
    db.commit()

    return {"session_token": token, "role": role}


@router.post("/logout")
def logout(session_token: str, db: Session = Depends(get_db)):
    row = db.query(SessionToken).filter(SessionToken.token == session_token).first()
    if row:
        db.delete(row)
        db.commit()
    return {"message": "Logged out"}