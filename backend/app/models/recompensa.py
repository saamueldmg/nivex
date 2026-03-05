from app.extensions import db

class Recompensa(db.Model):
    __tablename__ = 'recompensas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    costo_monedas = db.Column(db.Integer, nullable=False)
    icono = db.Column(db.String(100), nullable=True)
    activa = db.Column(db.Boolean, default=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)

    # Relaciones
    canjes = db.relationship('Canje', backref='recompensa', lazy=True)

    def __repr__(self):
        return f'<Recompensa {self.nombre} - {self.costo_monedas} monedas>'