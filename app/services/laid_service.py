import uuid
from sqlalchemy.orm import Session
from app.models.students_global import StudentGlobal
from app.models.student_institution_link import StudentInstitutionLink

def generate_laid() -> str:
    """Generate a unique LAID (Learning and Academic Identifier)"""
    return f"LAID-{uuid.uuid4().hex[:12].upper()}"

def create_student(db: Session, name: str, email: str, institution_id: int) -> StudentGlobal:
    """
    Create a student in the global database and link to institution.
    If student already exists, just link to new institution.
    """
    # Check if student already exists
    existing = db.query(StudentGlobal).filter(StudentGlobal.email == email).first()
    if existing:
        # Link institution if not already linked
        link = db.query(StudentInstitutionLink).filter(
            StudentInstitutionLink.laid == existing.laid,
            StudentInstitutionLink.institution_id == institution_id
        ).first()
        if not link:
            new_link = StudentInstitutionLink(
                laid=existing.laid,
                institution_id=institution_id
            )
            db.add(new_link)
            db.commit()
        return existing
    
    # Create new student with unique LAID
    laid = generate_laid()
    student = StudentGlobal(
        laid=laid,
        name=name,
        email=email
    )
    db.add(student)
    db.flush()  # Ensure student is in session before creating link

    # Link institution
    link = StudentInstitutionLink(
        laid=laid,
        institution_id=institution_id
    )
    db.add(link)
    db.commit()
    db.refresh(student)
    
    return student

def get_student_by_email(db: Session, email: str) -> StudentGlobal:
    """Get a student by email"""
    return db.query(StudentGlobal).filter(StudentGlobal.email == email).first()

def get_student_by_laid(db: Session, laid: str) -> StudentGlobal:
    """Get a student by LAID"""
    return db.query(StudentGlobal).filter(StudentGlobal.laid == laid).first()

def get_all_students(db: Session) -> list:
    """Get all students in the system"""
    return db.query(StudentGlobal).all()

def get_student_institutions(db: Session, laid: str) -> list:
    """Get all institutions a student is linked to"""
    return db.query(StudentInstitutionLink).filter(
        StudentInstitutionLink.laid == laid
    ).all()