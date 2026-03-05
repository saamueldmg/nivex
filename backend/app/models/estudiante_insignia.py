from app.extensions import db
from datetime import datetime

class EstudianteInsignia(db.Model):
    __tablename__ = 'estudiante_insignias'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    insignia_id = db.Column(db.Integer, db.ForeignKey('insignias.id'), nullable=False)
    fecha_obtencion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<EstudianteInsignia estudiante={self.estudiante_id} insignia={self.insignia_id}>'