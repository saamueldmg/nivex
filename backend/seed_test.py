from app import create_app
from app.extensions import db
from app.models.clase import Clase
from app.models.actividad import Actividad
from app.models.progreso_nivel import ProgresoNivel
from app.models.docente import Docente
from app.models.estudiante import Estudiante

app = create_app()

with app.app_context():
    # Buscar docente y estudiante ya creados
    docente = Docente.query.first()
    estudiante = Estudiante.query.first()

    if not docente:
        print("ERROR: No hay docente. Crea uno primero en Postman.")
    elif not estudiante:
        print("ERROR: No hay estudiante. Crea uno primero en Postman.")
    else:
        # Crear clase
        clase = Clase(
            grado="11",
            grupo="A",
            docente_id=docente.id,
            periodo_academico="2026-1",
            clima_actual="SOLEADO"
        )
        db.session.add(clase)
        db.session.flush()

        # Asignar clase al estudiante
        estudiante.clase_id = clase.id

        # Crear actividad
        actividad = Actividad(
            nombre="Taller 1 - Variables",
            tipo="TAREA",
            puntuacion_maxima=5.0,
            xp_base=500,
            clase_id=clase.id,
            docente_id=docente.id
        )
        db.session.add(actividad)
        db.session.flush()

        # Crear ProgresoNivel para el estudiante en Nivel 1
        progreso = ProgresoNivel(
            estudiante_id=estudiante.id,
            nivel_id=1,
            xp_acumulado=0,
            desempeno="BAJO",
            estado="EN_CURSO"
        )
        db.session.add(progreso)
        db.session.commit()

        print(f"✅ Clase creada con ID: {clase.id}")
        print(f"✅ Actividad creada con ID: {actividad.id}")
        print(f"✅ ProgresoNivel creado para estudiante ID: {estudiante.id}")