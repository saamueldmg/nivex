from app.extensions import db

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    grado = db.Column(db.String(20), nullable=False)
    grupo = db.Column(db.String(10), nullable=False)
    clase_id = db.Column(db.Integer, db.ForeignKey('clases.id'), nullable=True)

    # Progreso del juego
    monedas = db.Column(db.Integer, default=0)
    vida = db.Column(db.Integer, default=100)
    nivel_actual = db.Column(db.Integer, default=1)
    racha_actual = db.Column(db.Integer, default=0)
    racha_maxima = db.Column(db.Integer, default=0)
    multiplicador = db.Column(db.Float, default=1.0)

    # Estado final
    congelado = db.Column(db.Boolean, default=False)
    estado_final = db.Column(db.String(20), nullable=True)
    xp_promedio_final = db.Column(db.Float, nullable=True)
    game_over = db.Column(db.Boolean, default=False)

    # Personalizacion
    avatar_config = db.Column(db.JSON, default={})
    tema_activo = db.Column(db.String(30), default='claro')
    titulo_activo_id = db.Column(db.Integer, db.ForeignKey('titulos.id'), nullable=True)

    # Relaciones
    progreso_niveles = db.relationship('ProgresoNivel', backref='estudiante', lazy=True)
    calificaciones = db.relationship('Calificacion', backref='estudiante', lazy=True)
    insignias = db.relationship('EstudianteInsignia', backref='estudiante', lazy=True)
    canjes = db.relationship('Canje', backref='estudiante', lazy=True)

    def __repr__(self):
        return f'<Estudiante {self.nombre}>'