from app.extensions import db
from datetime import datetime

class Actividad(db.Model):
    __tablename__ = 'actividades'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(
        db.Enum('TAREA', 'EXAMEN', 'PROYECTO', 'PARTICIPACION', name='tipo_actividad_enum'),
        nullable=False
    )
    fecha_limite = db.Column(db.DateTime, nullable=True)
    puntuacion_maxima = db.Column(db.Float, nullable=False, default=5.0)
    xp_base = db.Column(db.Integer, nullable=False, default=500)
    clase_id = db.Column(db.Integer, db.ForeignKey('clases.id'), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    calificaciones = db.relationship('Calificacion', backref='actividad', lazy=True)

    def __repr__(self):
        return f'<Actividad {self.nombre} - {self.tipo}>'