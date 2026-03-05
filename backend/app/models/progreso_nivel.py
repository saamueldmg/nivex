from app.extensions import db
from datetime import datetime

class ProgresoNivel(db.Model):
    __tablename__ = 'progreso_niveles'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    nivel_id = db.Column(db.Integer, db.ForeignKey('niveles.id'), nullable=False)

    # XP
    xp_acumulado = db.Column(db.Integer, default=0)
    xp_antes_recuperacion = db.Column(db.Integer, nullable=True)

    # Desempeño
    desempeno = db.Column(
        db.Enum('BAJO', 'BASICO', 'ALTO', 'SUPERIOR', name='desempeno_enum'),
        default='BAJO'
    )

    # Estado
    estado = db.Column(
        db.Enum(
            'EN_CURSO',
            'APROBADO',
            'APROBADO_RECUPERACION',
            'SUSPENDIDO',
            'PENDIENTE',
            name='estado_nivel_enum'
        ),
        default='EN_CURSO'
    )

    # Fechas
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime, nullable=True)
    fecha_limite_recuperacion = db.Column(db.DateTime, nullable=True)

    # Recuperacion
    recuperacion_activa = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ProgresoNivel estudiante={self.estudiante_id} nivel={self.nivel_id} xp={self.xp_acumulado}>'