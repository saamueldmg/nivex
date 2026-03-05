from app.extensions import db, jwt
from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.models.docente import Docente
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from marshmallow import ValidationError
import bcrypt
from datetime import timedelta

# Blacklist en memoria (en produccion usar Redis)
blacklisted_tokens = set()

class AuthService:

    @staticmethod
    def registrar(data: dict) -> dict:
        """
        Registra un nuevo usuario (estudiante o docente).
        data esperado: email, password, rol, nombre
        Para ESTUDIANTE: grado, grupo, clase_id (opcional)
        """
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        rol = data.get("rol", "").upper()
        nombre = data.get("nombre", "").strip()

        # Validaciones básicas
        if not email or not password or not rol or not nombre:
            raise ValueError("email, password, rol y nombre son obligatorios.")

        if rol not in ("ESTUDIANTE", "DOCENTE", "ADMIN"):
            raise ValueError("rol debe ser ESTUDIANTE, DOCENTE o ADMIN.")

        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")

        # Verificar email único
        if Usuario.query.filter_by(email=email).first():
            raise ValueError("Ya existe una cuenta con ese email.")

        # Hash de contraseña
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(rounds=12)
        ).decode("utf-8")

        # Crear usuario base
        usuario = Usuario(
            email=email,
            password_hash=password_hash,
            rol=rol,
            activo=True
        )
        db.session.add(usuario)
        db.session.flush()  # Obtener ID sin commit

        # Crear perfil según rol
        if rol == "ESTUDIANTE":
            grado = data.get("grado", "").strip()
            grupo = data.get("grupo", "").strip()
            if not grado or not grupo:
                raise ValueError("grado y grupo son obligatorios para estudiantes.")

            estudiante = Estudiante(
                usuario_id=usuario.id,
                nombre=nombre,
                grado=grado,
                grupo=grupo,
                monedas=0,
                vida=100,
                nivel_actual=1,
                racha_actual=0,
                racha_maxima=0,
                multiplicador=1.0,
                congelado=False,
                game_over=False,
                avatar_config={}
            )
            db.session.add(estudiante)

        elif rol == "DOCENTE":
            asignatura = data.get("asignatura", "Desarrollo de Software")
            docente = Docente(
                usuario_id=usuario.id,
                nombre=nombre,
                asignatura=asignatura
            )
            db.session.add(docente)

        db.session.commit()

        return {
            "mensaje": "Usuario registrado exitosamente.",
            "usuario_id": usuario.id,
            "rol": usuario.rol
        }

    @staticmethod
    def login(email: str, password: str) -> dict:
        """
        Autentica un usuario. Retorna access_token y refresh_token.
        """
        if not email or not password:
            raise ValueError("email y password son obligatorios.")

        email = email.strip().lower()

        usuario = Usuario.query.filter_by(email=email, activo=True).first()
        if not usuario:
            raise ValueError("Credenciales inválidas.")

        if not bcrypt.checkpw(password.encode("utf-8"), usuario.password_hash.encode("utf-8")):
            raise ValueError("Credenciales inválidas.")

        # Claims adicionales en el token
        additional_claims = {"rol": usuario.rol}

        # Obtener perfil_id según rol
        if usuario.rol == "ESTUDIANTE":
            perfil = Estudiante.query.filter_by(usuario_id=usuario.id).first()
            if perfil:
                additional_claims["estudiante_id"] = perfil.id
                additional_claims["nombre"] = perfil.nombre
        elif usuario.rol == "DOCENTE":
            perfil = Docente.query.filter_by(usuario_id=usuario.id).first()
            if perfil:
                additional_claims["docente_id"] = perfil.id
                additional_claims["nombre"] = perfil.nombre

        access_token = create_access_token(
            identity=str(usuario.id),
            additional_claims=additional_claims,
            expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_refresh_token(
            identity=str(usuario.id),
            expires_delta=timedelta(days=7)
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "rol": usuario.rol,
            "usuario_id": usuario.id
        }

    @staticmethod
    def logout(jti: str) -> dict:
        """
        Agrega el JTI del token a la blacklist.
        """
        blacklisted_tokens.add(jti)
        return {"mensaje": "Sesión cerrada exitosamente."}

    @staticmethod
    def cambiar_password(usuario_id: int, password_actual: str, password_nueva: str) -> dict:
        """
        Cambia la contraseña verificando la actual.
        """
        if len(password_nueva) < 8:
            raise ValueError("La nueva contraseña debe tener al menos 8 caracteres.")

        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        if not bcrypt.checkpw(password_actual.encode("utf-8"), usuario.password_hash.encode("utf-8")):
            raise ValueError("La contraseña actual es incorrecta.")

        usuario.password_hash = bcrypt.hashpw(
            password_nueva.encode("utf-8"),
            bcrypt.gensalt(rounds=12)
        ).decode("utf-8")

        db.session.commit()
        return {"mensaje": "Contraseña actualizada exitosamente."}