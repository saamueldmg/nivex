from app.extensions import db
from app.models.calificacion import Calificacion
from app.models.actividad import Actividad
from app.models.estudiante import Estudiante
from app.models.progreso_nivel import ProgresoNivel


class GradeService:

    @staticmethod
    def registrar_calificacion(data: dict) -> dict:
        """
        Registra una calificación y calcula XP y monedas básicos.
        data esperado: estudiante_id, actividad_id, nota
        """
        estudiante_id = data.get("estudiante_id")
        actividad_id = data.get("actividad_id")
        nota = data.get("nota")

        # Validaciones básicas
        if estudiante_id is None or actividad_id is None or nota is None:
            raise ValueError("estudiante_id, actividad_id y nota son obligatorios.")

        if not isinstance(nota, (int, float)) or nota < 0 or nota > 5:
            raise ValueError("La nota debe ser un número entre 0 y 5.")

        # Verificar que existen
        estudiante = Estudiante.query.get(estudiante_id)
        if not estudiante:
            raise ValueError("Estudiante no encontrado.")

        actividad = Actividad.query.get(actividad_id)
        if not actividad:
            raise ValueError("Actividad no encontrada.")

        # Verificar si ya tiene calificación en esta actividad
        calificacion_existente = Calificacion.query.filter_by(
            estudiante_id=estudiante_id,
            actividad_id=actividad_id
        ).first()
        if calificacion_existente:
            raise ValueError("Este estudiante ya tiene una calificación en esta actividad.")

        # Calcular XP y monedas
        xp_otorgados, monedas_otorgadas = GradeService._calcular_xp_monedas(
            nota, actividad, estudiante
        )

        # Guardar calificación
        calificacion = Calificacion(
            estudiante_id=estudiante_id,
            actividad_id=actividad_id,
            nota=nota,
            xp_otorgados=xp_otorgados,
            monedas_otorgadas=monedas_otorgadas
        )
        db.session.add(calificacion)

        # Actualizar monedas del estudiante
        estudiante.monedas += monedas_otorgadas

        # Actualizar racha
        GradeService._actualizar_racha(estudiante, nota)

        # Actualizar XP en ProgresoNivel actual
        progreso = ProgresoNivel.query.filter_by(
            estudiante_id=estudiante_id,
            nivel_id=estudiante.nivel_actual,
            estado='EN_CURSO'
        ).first()

        if progreso:
            progreso.xp_acumulado += xp_otorgados
            progreso.desempeno = GradeService._calcular_desempeno(progreso.xp_acumulado)

        db.session.commit()

        return {
            "mensaje": "Calificación registrada exitosamente.",
            "calificacion_id": calificacion.id,
            "nota": nota,
            "xp_otorgados": xp_otorgados,
            "monedas_otorgadas": monedas_otorgadas,
            "racha_actual": estudiante.racha_actual,
            "multiplicador": estudiante.multiplicador,
            "xp_total_nivel": progreso.xp_acumulado if progreso else 0,
            "desempeno": progreso.desempeno if progreso else "BAJO"
        }

    @staticmethod
    def obtener_calificaciones_estudiante(estudiante_id: int) -> list:
        """
        Retorna todas las calificaciones de un estudiante.
        """
        calificaciones = Calificacion.query.filter_by(
            estudiante_id=estudiante_id
        ).all()

        return [
            {
                "calificacion_id": c.id,
                "actividad_id": c.actividad_id,
                "nota": c.nota,
                "xp_otorgados": c.xp_otorgados,
                "monedas_otorgadas": c.monedas_otorgadas,
                "fecha_registro": c.fecha_registro.isoformat() if c.fecha_registro else None
            }
            for c in calificaciones
        ]

    @staticmethod
    def obtener_calificaciones_actividad(actividad_id: int) -> list:
        """
        Retorna todas las calificaciones de una actividad.
        """
        calificaciones = Calificacion.query.filter_by(
            actividad_id=actividad_id
        ).all()

        return [
            {
                "calificacion_id": c.id,
                "estudiante_id": c.estudiante_id,
                "nota": c.nota,
                "xp_otorgados": c.xp_otorgados,
                "monedas_otorgadas": c.monedas_otorgadas,
                "fecha_registro": c.fecha_registro.isoformat() if c.fecha_registro else None
            }
            for c in calificaciones
        ]

    # ─── Métodos privados ─────────────────────────────────────────────────────

    @staticmethod
    def _calcular_xp_monedas(nota, actividad, estudiante):
        """
        XP = (nota / puntuacion_maxima) * xp_base_actividad
        Monedas = XP * tasa_monedas * multiplicador_racha
        """
        xp = (nota / actividad.puntuacion_maxima) * actividad.xp_base
        xp = round(xp)

        tasa_monedas = 0.5  # default, luego viene de ConfiguracionGamificacion
        monedas = round(xp * tasa_monedas * estudiante.multiplicador)

        return xp, monedas

    @staticmethod
    def _actualizar_racha(estudiante, nota):
        """
        Si nota >= 3.0 sube la racha, si no la resetea a 0.
        Actualiza el multiplicador según la racha.
        """
        if nota >= 3.0:
            estudiante.racha_actual += 1
            if estudiante.racha_actual > estudiante.racha_maxima:
                estudiante.racha_maxima = estudiante.racha_actual
        else:
            estudiante.racha_actual = 0

        # Actualizar multiplicador
        estudiante.multiplicador = GradeService._calcular_multiplicador(
            estudiante.racha_actual
        )

    @staticmethod
    def _calcular_multiplicador(racha):
        """
        1-2 = x1.0 | 3-4 = x1.25 | 5-7 = x1.5 | 8-9 = x1.75 | 10+ = x2.0
        """
        if racha >= 10:
            return 2.0
        elif racha >= 8:
            return 1.75
        elif racha >= 5:
            return 1.5
        elif racha >= 3:
            return 1.25
        else:
            return 1.0

    @staticmethod
    def _calcular_desempeno(xp):
        """
        BAJO < 3000 | BASICO 3000-3999 | ALTO 4000-4599 | SUPERIOR 4600+
        """
        if xp >= 4600:
            return "SUPERIOR"
        elif xp >= 4000:
            return "ALTO"
        elif xp >= 3000:
            return "BASICO"
        else:
            return "BAJO"