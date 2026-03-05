from app.extensions import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('ESTUDIANTE', 'DOCENTE', 'ADMIN', name='rol_enum'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    # Relaciones
    estudiante = db.relationship('Estudiante', backref='usuario', uselist=False)
    docente = db.relationship('Docente', backref='usuario', uselist=False)

    def __repr__(self):
        return f'<Usuario {self.email} - {self.rol}>'