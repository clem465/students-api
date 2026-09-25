from fastapi import FastAPI, HTTPException, Query

from src.data import students

app = FastAPI(
    title="Students API",
    description="API REST pour gérer un annuaire d'étudiants",
    version="1.0.0",
)


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