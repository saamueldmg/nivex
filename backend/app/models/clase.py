from app.extensions import db

class Clase(db.Model):
    __tablename__ = 'clases'

    id = db.Column(db.Integer, primary_key=True)
    grado = db.Column(db.String(20), nullable=False)
    grupo = db.Column(db.String(10), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    periodo_academico = db.Column(db.String(20), nullable=False)
    clima_actual = db.Column(
        db.Enum('SOLEADO', 'NUBLADO', 'LLUVIOSO', 'TORMENTA', 'ARCOIRIS', name='clima_enum'),
        default='SOLEADO'
    )

    # Relaciones
    estudiantes = db.relationship('Estudiante', backref='clase', lazy=True)
    actividades = db.relationship('Actividad', backref='clase', lazy=True)

    def __repr__(self):
        return f'<Clase {self.grado}-{self.grupo}>'