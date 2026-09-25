from fastapi.testclient import TestClient

from src.app import app
from src.data import reset_data


client = TestClient(app)


def setup_function():
    """Reset data before each test."""
    reset_data()


def test_get_students_returns_200_and_list():
    response = client.get("/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_students_returns_initial_students():
    response = client.get("/students")

    students = response.json()

    assert len(students) == 5
    assert students[0]["firstName"] == "Alice"


def test_get_student_by_valid_id():
    response = client.get("/students/1")

    assert response.status_code == 200

    student = response.json()

    assert student["id"] == 1
    assert student["firstName"] == "Alice"


def test_get_student_with_unknown_id():
    response = client.get("/students/999")

    assert response.status_code == 404


def test_get_student_with_invalid_id():
    response = client.get("/students/abc")

    assert response.status_code == 400


def test_get_students_stats():
    response = client.get("/students/stats")

    assert response.status_code == 200

    stats = response.json()

    assert stats["totalStudents"] == 5
    assert stats["averageGrade"] == 15.7
    assert stats["studentsByField"]["informatique"] == 2
    assert stats["bestStudent"]["id"] == 3


def test_search_students_by_first_name():
    response = client.get("/students/search?q=alice")

    assert response.status_code == 200

    results = response.json()

    assert len(results) == 1
    assert results[0]["firstName"] == "Alice"


def test_search_students_is_case_insensitive():
    response = client.get("/students/search?q=MARTIN")

    assert response.status_code == 200

    results = response.json()

    assert len(results) == 1
    assert results[0]["lastName"] == "Martin"


def test_search_students_without_query():
    response = client.get("/students/search")

    assert response.status_code == 400


def test_search_students_with_empty_query():
    response = client.get("/students/search?q=")

    assert response.status_code == 400