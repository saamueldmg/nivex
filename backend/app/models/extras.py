from app.extensions import db
from datetime import datetime

class EstudianteTema(db.Model):
    __tablename__ = 'estudiante_temas'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    tema = db.Column(db.String(50), nullable=False)
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow)

class RetoClase(db.Model):
    __tablename__ = 'retos_clase'

    id = db.Column(db.Integer, primary_key=True)
    clase_id = db.Column(db.Integer, db.ForeignKey('clases.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    condicion_tipo = db.Column(db.String(50), nullable=True)
    condicion_valor = db.Column(db.Float, nullable=True)
    recompensa_tipo = db.Column(db.String(50), nullable=True)
    recompensa_valor = db.Column(db.Float, nullable=True)
    progreso_actual = db.Column(db.Float, default=0)
    completado = db.Column(db.Boolean, default=False)

class MuroFama(db.Model):
    __tablename__ = 'muro_fama'

    id = db.Column(db.Integer, primary_key=True)
    clase_id = db.Column(db.Integer, db.ForeignKey('clases.id'), nullable=False)
    semana = db.Column(db.String(20), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    valor = db.Column(db.Float, nullable=True)
    monedas_otorgadas = db.Column(db.Integer, default=0)

class LogroSecreto(db.Model):
    __tablename__ = 'logros_secretos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    narrativa = db.Column(db.Text, nullable=True)
    condicion = db.Column(db.String(100), nullable=True)
    monedas_bonus = db.Column(db.Integer, default=0)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorios.id'), nullable=True)
    titulo_id = db.Column(db.Integer, db.ForeignKey('titulos.id'), nullable=True)

class EstudianteLogroSecreto(db.Model):
    __tablename__ = 'estudiante_logros_secretos'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    logro_id = db.Column(db.Integer, db.ForeignKey('logros_secretos.id'), nullable=False)
    fecha_descubrimiento = db.Column(db.DateTime, default=datetime.utcnow)