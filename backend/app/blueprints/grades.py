from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.grade_service import GradeService

grades_bp = Blueprint("grades", __name__, url_prefix="/api/v1/grades")


def solo_docente():
    claims = get_jwt()
    return claims.get("rol") == "DOCENTE"


# ─── POST /api/v1/grades/ ────────────────────────────────────────────────────

@grades_bp.route("/", methods=["POST"])
@jwt_required()
def registrar_calificacion():
    if not solo_docente():
        return jsonify({"error": "Solo los docentes pueden registrar calificaciones."}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Body JSON requerido."}), 400

    try:
        resultado = GradeService.registrar_calificacion(data)
        return jsonify(resultado), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


# ─── GET /api/v1/grades/estudiante/<id> ──────────────────────────────────────

@grades_bp.route("/estudiante/<int:estudiante_id>", methods=["GET"])
@jwt_required()
def calificaciones_estudiante(estudiante_id):
    try:
        resultado = GradeService.obtener_calificaciones_estudiante(estudiante_id)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


# ─── GET /api/v1/grades/actividad/<id> ───────────────────────────────────────

@grades_bp.route("/actividad/<int:actividad_id>", methods=["GET"])
@jwt_required()
def calificaciones_actividad(actividad_id):
    try:
        resultado = GradeService.obtener_calificaciones_actividad(actividad_id)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500