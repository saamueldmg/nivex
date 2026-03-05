from app.extensions import db

class MetaPersonal(db.Model):
    __tablename__ = 'metas_personales'

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    tipo_meta = db.Column(db.String(50), nullable=False)
    valor_objetivo = db.Column(db.Float, nullable=False)
    valor_actual = db.Column(db.Float, default=0)
    activa = db.Column(db.Boolean, default=True)
    completada = db.Column(db.Boolean, default=False)
    monedas_bonus = db.Column(db.Integer, default=0)