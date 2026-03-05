from app.extensions import db
from datetime import datetime

class Canje(db.Model):
    __tablename__ = 'canjes'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    recompensa_id = db.Column(db.Integer, db.ForeignKey('recompensas.id'), nullable=False)
    monedas_gastadas = db.Column(db.Integer, nullable=False)
    fecha_canje = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(
        db.Enum('PENDIENTE', 'APLICADA', 'RECHAZADA', name='estado_canje_enum'),
        default='PENDIENTE'
    )
    aplicada = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Canje estudiante={self.estudiante_id} recompensa={self.recompensa_id}>'