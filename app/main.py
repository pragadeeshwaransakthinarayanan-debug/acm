from fastapi import FastAPI
from app.database import Base, engine

# Import models so create_all detects tables
from app.models.students import Student
from app.models.attendance import Attendance
from app.models.marks import Mark
from app.models.fees import Fee
from app.models.enrollment import Enrollment
from app.models.teacher_global import TeacherGlobal
from app.models.teacher_institution_link import TeacherInstitutionLink
from app.models.teacher_salary import TeacherSalary
from app.models.teacher_course_assignment import TeacherCourseAssignment
from app.models.admin_global import AdminGlobal
from app.models.admin_institution_link import AdminInstitutionLink

app = FastAPI(title="ERP Backend API")

Base.metadata.create_all(bind=engine)

from app.routes.student_portal import router as student_router
from app.routes.teacher_portal import router as teacher_router
from app.routes.admin_portal import router as admin_router
from app.routes.auth_session import router as auth_session_router
from app.routes.compliance import router as compliance_router

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(admin_router)
app.include_router(auth_session_router)
app.include_router(compliance_router)

@app.get("/")
def root():
    return {"message": "Backend Server Running"}