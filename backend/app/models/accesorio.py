from app.extensions import db
from datetime import datetime

class Accesorio(db.Model):
    __tablename__ = 'accesorios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=True)
    icono = db.Column(db.String(200), nullable=True)
    condicion_tipo = db.Column(db.String(50), nullable=True)
    condicion_valor = db.Column(db.Float, nullable=True)
    descripcion_desbloqueo = db.Column(db.String(200), nullable=True)

class EstudianteAccesorio(db.Model):
    __tablename__ = 'estudiante_accesorios'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    accesorio_id = db.Column(db.Integer, db.ForeignKey('accesorios.id'), nullable=False)
    fecha_desbloqueo = db.Column(db.DateTime, default=datetime.utcnow)
    equipado = db.Column(db.Boolean, default=False)