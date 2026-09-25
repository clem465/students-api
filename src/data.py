from copy import deepcopy

INITIAL_STUDENTS = [
    {
        "id": 1,
        "firstName": "Alice",
        "lastName": "Martin",
        "email": "alice.martin@example.com",
        "grade": 16.5,
        "field": "informatique",
    },
    {
        "id": 2,
        "firstName": "Thomas",
        "lastName": "Bernard",
        "email": "thomas.bernard@example.com",
        "grade": 14.0,
        "field": "mathématiques",
    },
    {
        "id": 3,
        "firstName": "Sophie",
        "lastName": "Dubois",
        "email": "sophie.dubois@example.com",
        "grade": 18.5,
        "field": "physique",
    },
    {
        "id": 4,
        "firstName": "Lucas",
        "lastName": "Petit",
        "email": "lucas.petit@example.com",
        "grade": 12.5,
        "field": "chimie",
    },
    {
        "id": 5,
        "firstName": "Emma",
        "lastName": "Robert",
        "email": "emma.robert@example.com",
        "grade": 17.0,
        "field": "informatique",
    },
]


students = deepcopy(INITIAL_STUDENTS)


def reset_data():
    """Reset the students list to its initial state."""
    students.clear()
    students.extend(deepcopy(INITIAL_STUDENTS))