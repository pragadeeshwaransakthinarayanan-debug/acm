from fastapi import FastAPI
from app.database import Base, engine

# ✅ Import models (IMPORTANT: so create_all sees tables)
from app.models.enrollment import Enrollment

# ✅ Use ONE naming style
# If your model file has class Fee, use Fee
from app.models.fees import Fees
from app.models.marks import Marks

from app.models.teacher_global import TeacherGlobal
from app.models.teacher_institution_link import TeacherInstitutionLink

# If you created these for teacher self features
# from app.models.teacher_attendance import TeacherAttendance
from app.models.teacher_salary import TeacherSalary
from app.models.teacher_course_assignment import TeacherCourseAssignment

app = FastAPI(title="ERP Backend API")

# ✅ Create tables after importing models
Base.metadata.create_all(bind=engine)

# ✅ Include routers
from app.routes.student_portal import router as student_portal_router
from app.routes.teacher_portal import router as teacher_portal_router
from app.routes.admin_portal import router as admin_portal_router  # Make sure app/routes/admin_portal.py exists and defines 'router'

app.include_router(student_portal_router)
app.include_router(teacher_portal_router)
app.include_router(admin_portal_router)

# Optional (keep only if you need these)
# from app.routes import laid, attendance, student
# app.include_router(laid.router)
# app.include_router(attendance.router)
# app.include_router(student.router)
from app.models.students import Student