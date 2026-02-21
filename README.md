# ERP Backend API

A complete Enterprise Resource Planning (ERP) system backend built with FastAPI and PostgreSQL.

## Features

### 1. **Student Management (LAID System)**
- Global student registry with Learning and Academic Identifier (LAID)
- Multi-institution student support
- Automatic LAID generation on student creation
- Student-institution linking

### 2. **Academic Management**
- Course management
- Student enrollment system
- Attendance tracking
- Grade management

### 3. **Architecture**
- **Models**: SQLAlchemy ORM models for database tables
- **Schemas**: Pydantic models for request/response validation
- **Routes**: FastAPI router endpoints
- **Services**: Business logic layer
- **Database**: PostgreSQL with connection management

## Project Structure

```
erp-backend/
├── app/
│   ├── __init__.py           # App factory
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models/              # SQLAlchemy models
│   │   ├── student.py       # Simple student model
│   │   ├── laid.py          # LAID system models
│   │   └── academic.py      # Academic models
│   ├── routes/              # API endpoints
│   │   ├── laid.py          # Student management endpoints
│   │   └── student.py       # Academic endpoints
│   ├── schemas/             # Pydantic schemas
│   │   ├── student.py       # Student schemas
│   │   ├── laid.py          # LAID system schemas
│   │   └── academic.py      # Academic schemas
│   └── services/            # Business logic
│       └── laid_service.py  # LAID operations
├── requirements.txt         # Python dependencies
└── .env.example            # Environment variables template
```

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- PostgreSQL database running
- Virtual environment (venv or conda)

### 2. Installation

```bash
# Navigate to project directory
cd erp-backend

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file from the template:
```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:
```
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/erp_db
```

### 4. Database Setup

The application automatically creates tables on startup using SQLAlchemy's metadata.

### 5. Run the Server

```bash
# Development mode with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or directly run main.py
python app/main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### Health & Info
- `GET /` - API information
- `GET /health` - Health check

### Student Management (LAID System)
**Prefix**: `/students`

- `POST /students/` - Create a new student
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "institution_id": 1
  }
  ```

- `GET /students/` - List all students

- `GET /students/{email}` - Get student by email

### Academic Management
**Prefix**: `/academic`

#### Courses
- `POST /academic/courses` - Create a course
  ```json
  {
    "name": "Advanced Python",
    "laid": "LAID-abc123def456",
    "institution_id": 1
  }
  ```
- `GET /academic/courses` - List courses (optional: `?institution_id=1`)
- `GET /academic/courses/{course_id}` - Get course details

#### Enrollments
- `POST /academic/enrollments` - Enroll student in course
  ```json
  {
    "course_id": 1,
    "laid": "LAID-abc123def456",
    "institution_id": 1
  }
  ```
- `GET /academic/enrollments` - List enrollments (optional filters: `?course_id=1`, `?laid=LAID-xxx`)

#### Attendance
- `POST /academic/attendance` - Mark attendance
  ```json
  {
    "course_id": 1,
    "laid": "LAID-abc123def456",
    "status": "Present",
    "institution_id": 1
  }
  ```
- `GET /academic/attendance` - List attendance records (optional filters)

#### Grades
- `POST /academic/grades` - Add/update grade
  ```json
  {
    "course_id": 1,
    "laid": "LAID-abc123def456",
    "grade": 95.5,
    "institution_id": 1
  }
  ```
- `GET /academic/grades` - List grades (optional filters)

## Interactive API Documentation

Once the server is running:

- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc (Alternative)**: http://localhost:8000/redoc

## Database Schema

### Students (LAID System)
- `students_global`: Global student registry with LAID
- `student_institution_link`: Many-to-many relationship for students and institutions

### Academic
- `course`: Course information
- `enrollment`: Student enrollments
- `attendance`: Attendance records
- `grade`: Student grades

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad request (duplicate entries, validation errors)
- `404` - Not found (student, course, etc.)
- `500` - Server error

## Development Notes

### Adding New Features
1. Create model in `app/models/`
2. Create schema in `app/schemas/`
3. Create service logic in `app/services/`
4. Create routes in `app/routes/`
5. Include router in `app/__init__.py`

### Database Migrations
For complex migrations, consider using Alembic:
```bash
pip install alembic
alembic init alembic
```

## Troubleshooting

**ModuleNotFoundError**: Ensure virtual environment is activated and dependencies are installed

**Database Connection Error**: Verify PostgreSQL is running and credentials in `.env` are correct

**Port Already in Use**: Change port with `--port 8001` flag

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Role-based access control (RBAC)
- [ ] Audit logging
- [ ] Data export (CSV, JSON)
- [ ] Advanced reporting
- [ ] Batch operations
- [ ] Rate limiting
- [ ] API versioning

## License

This project is part of the ERP system.
