from app.extensions import db

class Insignia(db.Model):
    __tablename__ = 'insignias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    icono = db.Column(db.String(100), nullable=True)
    condicion = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

    # Relaciones
    estudiantes = db.relationship('EstudianteInsignia', backref='insignia', lazy=True)

    def __repr__(self):
        return f'<Insignia {self.nombre}>'