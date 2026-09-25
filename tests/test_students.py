from src.data import INITIAL_STUDENTS, reset_data, students


def test_initial_students():
    assert len(students) == 5
    assert len(INITIAL_STUDENTS) == 5


def test_reset_data():
    reset_data()

    assert len(students) == 5
    assert students[0]["id"] == 1
    assert students[0]["firstName"] == "Alice"