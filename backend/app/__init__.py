from flask import Flask
from app.extensions import db, jwt, cors, limiter
from app.config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)

    # Importar modelos para que SQLAlchemy los registre
    from app.models import (
    Usuario, Estudiante, Docente, Clase,
    Nivel, ProgresoNivel, Actividad, Calificacion,
    Insignia, EstudianteInsignia, Recompensa,
    Canje, ConfiguracionGamificacion,
    )
    from app.models.titulo import Titulo, EstudianteTitulo
    from app.models.accesorio import Accesorio, EstudianteAccesorio
    from app.models.meta_personal import MetaPersonal
    from app.models.extras import EstudianteTema, RetoClase, MuroFama, LogroSecreto, EstudianteLogroSecreto

   

    

    # Crear tablas
    with app.app_context():
        db.create_all()

    # Registrar blueprints
    from app.blueprints.auth import auth_bp, token_esta_en_blacklist
    jwt.token_in_blocklist_loader(token_esta_en_blacklist)
    app.register_blueprint(auth_bp)
    from app.blueprints.grades import grades_bp
    app.register_blueprint(grades_bp)

    return app