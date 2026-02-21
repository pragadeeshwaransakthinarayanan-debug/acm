from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session import SessionToken

def get_current_student(
    x_session_token: str = Header(None),
    db: Session = Depends(get_db),
):
    if not x_session_token:
        raise HTTPException(status_code=401, detail="Missing X-Session-Token")

    sess = db.query(SessionToken).filter(SessionToken.token == x_session_token).first()
    if not sess:
        raise HTTPException(status_code=401, detail="Invalid session token")

    if sess.role != "student":
        raise HTTPException(status_code=403, detail="Not a student session")

    return {"laid": sess.laid, "institution_id": sess.institution_id}
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session import SessionToken  # or your existing session model


def get_current_teacher(
    db: Session = Depends(get_db),
    x_session_token: str | None = Header(default=None),
):
    if not x_session_token:
        raise HTTPException(status_code=401, detail="Missing X-Session-Token header")

    s = db.query(SessionToken).filter(SessionToken.token == x_session_token).first()
    if not s:
        raise HTTPException(status_code=401, detail="Invalid session token")

    if s.role != "teacher":
        raise HTTPException(status_code=403, detail="Not a teacher session")

    return s  # s.laid, s.institution_id