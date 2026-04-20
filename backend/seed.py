from backend.app import create_app
from extensions import db
from models import Grade, Student


def run_seed():
    app = create_app()

    with app.app_context():
        # Borrar datos anteriores (opcional en esta etapa)
        Student.query.delete()
        Grade.query.delete()
        db.session.commit()

        # Crear un grado de prueba
        grade_11_2 = Grade(name="11_2", max_students=40)
        db.session.add(grade_11_2)
        db.session.commit()

        # Crear un estudiante de prueba
        student = Student(
            full_name="Juan Pérez",
            grade_id=grade_11_2.id,
            life=100,
            xp=0,
            coins=0,
            level=1,
            is_dead=False,
            life_reason=None,
        )
        db.session.add(student)
        db.session.commit()

        print("Datos de prueba creados:")
        print("Grado:", grade_11_2)
        print("Estudiante:", student)


if __name__ == "__main__":
    run_seed()