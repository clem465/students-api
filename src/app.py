from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field

from src.data import students

app = FastAPI(
    title="Students API",
    description="API REST pour gérer un annuaire d'étudiants",
    version="1.0.0",
)


class StudentCreate(BaseModel):
    firstName: str = Field(min_length=2)
    lastName: str = Field(min_length=2)
    email: EmailStr
    grade: float = Field(ge=0, le=20)
    field: str

class StudentUpdate(BaseModel):
    firstName: str = Field(min_length=2)
    lastName: str = Field(min_length=2)
    email: EmailStr
    grade: float = Field(ge=0, le=20)
    field: str

@app.get("/students")
def get_students():
    """Return all students."""
    return students


@app.get("/students/stats")
def get_statistics():
    """Return statistics about students."""
    total_students = len(students)

    if total_students == 0:
        average_grade = 0
        best_student = None
    else:
        total_grade = sum(student["grade"] for student in students)
        average_grade = round(total_grade / total_students, 2)
        best_student = max(students, key=lambda student: student["grade"])

    students_by_field = {}

    for student in students:
        field = student["field"]
        students_by_field[field] = students_by_field.get(field, 0) + 1

    return {
        "totalStudents": total_students,
        "averageGrade": average_grade,
        "studentsByField": students_by_field,
        "bestStudent": best_student,
    }


@app.get("/students/search")
def search_students(
    q: str | None = Query(default=None),
):
    """Search students by first name or last name."""
    if q is None or not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Le paramètre q est obligatoire.",
        )

    search_term = q.strip().lower()

    results = [
        student
        for student in students
        if search_term in student["firstName"].lower()
        or search_term in student["lastName"].lower()
    ]

    return results


@app.get("/students/{student_id}")
def get_student(student_id: str):
    """Return a student by ID."""
    if not student_id.isdigit():
        raise HTTPException(
            status_code=400,
            detail="L'identifiant doit être un nombre.",
        )

    student_id_int = int(student_id)

    for student in students:
        if student["id"] == student_id_int:
            return student

    raise HTTPException(
        status_code=404,
        detail="Étudiant introuvable.",
    )


@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    """Create a new student."""
    allowed_fields = {
        "informatique",
        "mathématiques",
        "physique",
        "chimie",
    }

    if student.field not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail="La filière est invalide.",
        )

    for existing_student in students:
        if existing_student["email"].lower() == student.email.lower():
            raise HTTPException(
                status_code=409,
                detail="Cette adresse email est déjà utilisée.",
            )

    if students:
        new_id = max(existing_student["id"] for existing_student in students) + 1
    else:
        new_id = 1

    new_student = {
        "id": new_id,
        "firstName": student.firstName,
        "lastName": student.lastName,
        "email": str(student.email),
        "grade": student.grade,
        "field": student.field,
    }

    students.append(new_student)

    return new_student

@app.put("/students/{student_id}")
def update_student(student_id: str, student: StudentUpdate):
    """Update an existing student."""
    if not student_id.isdigit():
        raise HTTPException(
            status_code=400,
            detail="L'identifiant doit être un nombre.",
        )

    student_id_int = int(student_id)

    student_to_update = None

    for existing_student in students:
        if existing_student["id"] == student_id_int:
            student_to_update = existing_student
            break

    if student_to_update is None:
        raise HTTPException(
            status_code=404,
            detail="Étudiant introuvable.",
        )

    allowed_fields = {
        "informatique",
        "mathématiques",
        "physique",
        "chimie",
    }

    if student.field not in allowed_fields:
        raise HTTPException(
            status_code=400,
            detail="La filière est invalide.",
        )

    for existing_student in students:
        if (
            existing_student["id"] != student_id_int
            and existing_student["email"].lower() == student.email.lower()
        ):
            raise HTTPException(
                status_code=409,
                detail="Cette adresse email est déjà utilisée.",
            )

    student_to_update["firstName"] = student.firstName
    student_to_update["lastName"] = student.lastName
    student_to_update["email"] = str(student.email)
    student_to_update["grade"] = student.grade
    student_to_update["field"] = student.field

    return student_to_update