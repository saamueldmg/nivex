from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
    verify_jwt_in_request,
    create_access_token
)
from app.services.auth_service import AuthService, blacklisted_tokens
from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.models.docente import Docente
from app.extensions import limiter
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


# ─── Token checker (blacklist) ───────────────────────────────────────────────

def token_esta_en_blacklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in blacklisted_tokens


# Registrar el callback en extensions al inicializar la app:
# from app.blueprints.auth import token_esta_en_blacklist
# jwt.token_in_blocklist_loader(token_esta_en_blacklist)


# ─── POST /api/v1/auth/register ──────────────────────────────────────────────

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("10 per minute")
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Body JSON requerido."}), 400

    try:
        resultado = AuthService.registrar(data)
        return jsonify(resultado), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


# ─── POST /api/v1/auth/login ─────────────────────────────────────────────────

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Body JSON requerido."}), 400

    email = data.get("email")
    password = data.get("password")

    try:
        resultado = AuthService.login(email, password)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


# ─── POST /api/v1/auth/logout ────────────────────────────────────────────────

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    resultado = AuthService.logout(jti)
    return jsonify(resultado), 200


# ─── POST /api/v1/auth/refresh ───────────────────────────────────────────────

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    rol = claims.get("rol")

    new_access_token = create_access_token(
        identity=identity,
        additional_claims={"rol": rol},
        expires_delta=timedelta(minutes=15)
    )
    return jsonify({"access_token": new_access_token}), 200


# ─── GET /api/v1/auth/me ─────────────────────────────────────────────────────

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    usuario_id = int(get_jwt_identity())
    claims = get_jwt()
    rol = claims.get("rol")

    usuario = Usuario.query.get(usuario_id)
    if not usuario or not usuario.activo:
        return jsonify({"error": "Usuario no encontrado."}), 404

    respuesta = {
        "usuario_id": usuario.id,
        "email": usuario.email,
        "rol": rol
    }

    if rol == "ESTUDIANTE":
        perfil = Estudiante.query.filter_by(usuario_id=usuario_id).first()
        if perfil:
            respuesta.update({
                "estudiante_id": perfil.id,
                "nombre": perfil.nombre,
                "grado": perfil.grado,
                "grupo": perfil.grupo,
                "monedas": perfil.monedas,
                "vida": perfil.vida,
                "nivel_actual": perfil.nivel_actual,
                "congelado": perfil.congelado,
                "game_over": perfil.game_over,
                "racha_actual": perfil.racha_actual,
                "multiplicador": perfil.multiplicador
            })

    elif rol == "DOCENTE":
        perfil = Docente.query.filter_by(usuario_id=usuario_id).first()
        if perfil:
            respuesta.update({
                "docente_id": perfil.id,
                "nombre": perfil.nombre,
                "asignatura": perfil.asignatura
            })

    return jsonify(respuesta), 200


# ─── PUT /api/v1/auth/cambiar-password ───────────────────────────────────────

@auth_bp.route("/cambiar-password", methods=["PUT"])
@jwt_required()
def cambiar_password():
    usuario_id = int(get_jwt_identity())
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Body JSON requerido."}), 400

    password_actual = data.get("password_actual")
    password_nueva = data.get("password_nueva")

    try:
        resultado = AuthService.cambiar_password(usuario_id, password_actual, password_nueva)
        return jsonify(resultado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500