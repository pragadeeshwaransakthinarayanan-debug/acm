from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceOut

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)
# Create a new attendance record
@router.post("/", response_model=AttendanceOut)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    new_attendance = Attendance(
        student_id=attendance.student_id,
        course_id=attendance.course_id,
        date=attendance.date,
        status=attendance.status
    )
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance

# Get all attendance records
@router.get("/", response_model=list[AttendanceOut])
def get_attendance_records(db: Session = Depends(get_db)):
    return db.query(Attendance).all()

# Get a single attendance record by ID
@router.get("/{attendance_id}", response_model=AttendanceOut)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return record