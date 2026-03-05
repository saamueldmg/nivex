from app.extensions import db
from datetime import datetime

class Titulo(db.Model):
    __tablename__ = 'titulos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(30), default='LOGRO')
    condicion_tipo = db.Column(db.String(50), nullable=True)
    condicion_valor = db.Column(db.Float, nullable=True)
    costo_monedas = db.Column(db.Integer, default=0)

class EstudianteTitulo(db.Model):
    __tablename__ = 'estudiante_titulos'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    titulo_id = db.Column(db.Integer, db.ForeignKey('titulos.id'), nullable=False)
    fecha_obtencion = db.Column(db.DateTime, default=datetime.utcnow)
    equipado = db.Column(db.Boolean, default=False)