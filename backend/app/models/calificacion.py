from app.extensions import db
from datetime import datetime

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividades.id'), nullable=False)
    nota = db.Column(db.Float, nullable=False)
    xp_otorgados = db.Column(db.Integer, default=0)
    monedas_otorgadas = db.Column(db.Integer, default=0)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Calificacion estudiante={self.estudiante_id} nota={self.nota}>'