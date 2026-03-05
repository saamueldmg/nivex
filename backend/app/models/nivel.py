from app.extensions import db

class Nivel(db.Model):
    __tablename__ = 'niveles'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)  # 1, 2, 3 o 4
    titulo = db.Column(db.String(50), nullable=False)
    periodo_academico = db.Column(db.String(20), nullable=False)

    # XP
    xp_minimo_aprobacion = db.Column(db.Integer, default=3000)
    xp_maximo = db.Column(db.Integer, default=5000)
    xp_tope_recuperacion = db.Column(db.Integer, default=3500)

    # Relaciones
    progresos = db.relationship('ProgresoNivel', backref='nivel', lazy=True)

    def __repr__(self):
        return f'<Nivel {self.numero} - {self.titulo}>'