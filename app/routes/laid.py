from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.students_global import StudentGlobal
from app.schemas.laid import StudentCreate, StudentOut

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# GET all students
@router.get("/", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)):
    students = db.query(StudentGlobal).all()
    return students

# GET single student by ID
@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentGlobal).filter(StudentGlobal.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# DELETE a student
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentGlobal).filter(StudentGlobal.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"detail": "Student deleted"}

# POST create a student
@router.post("/", response_model=StudentOut)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check for duplicate laid or email
    if db.query(StudentGlobal).filter(
        (StudentGlobal.laid == student.laid) | 
        (StudentGlobal.email == student.email)
    ).first():
        raise HTTPException(status_code=400, detail="Student already exists")
    
    db_student = StudentGlobal(
        laid=student.laid,
        full_name=student.full_name,
        email=student.email
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student