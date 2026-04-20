import random

DEFAULT_AVATARS = [
    "avatar_01.png",
    "avatar_02.png",
    "avatar_03.png",
    "avatar_04.png",
    "avatar_05.png",
]

def generate_students_for_grade(grade_name, count):
    students = []

    for i in range(1, count + 1):
        students.append({
            "id": f"{grade_name}-{i}",
            "name": f"Estudiante {i}",
            "grade": grade_name,
            "avatar": random.choice(DEFAULT_AVATARS),
            "level": 1,
            "xp": 0,
            "coins": 0,
            "life": 100
        })

    return students