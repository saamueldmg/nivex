from app.extensions import db

class Docente(db.Model):
    __tablename__ = 'docentes'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    asignatura = db.Column(db.String(100), nullable=False)

    # Relaciones
    clases = db.relationship('Clase', backref='docente', lazy=True)
    actividades = db.relationship('Actividad', backref='docente', lazy=True)
    recompensas = db.relationship('Recompensa', backref='docente', lazy=True)

    def __repr__(self):
        return f'<Docente {self.nombre}>'