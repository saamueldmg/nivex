from app.extensions import db

class ConfiguracionGamificacion(db.Model):
    __tablename__ = 'configuracion_gamificacion'

    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)

    # Tasas
    tasa_monedas = db.Column(db.Float, default=0.1)
    vida_inicial = db.Column(db.Integer, default=100)

    # Penalizaciones
    penalizacion_reprobacion = db.Column(db.Integer, default=10)
    penalizacion_inactividad = db.Column(db.Integer, default=5)

    # Umbrales
    umbral_aprobacion = db.Column(db.Integer, default=3000)

    def __repr__(self):
        return f'<ConfiguracionGamificacion docente={self.docente_id}>'