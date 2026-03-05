from app import create_app
from app.extensions import db
from app.models.nivel import Nivel

app = create_app('development')

def seed_niveles():
    niveles = [
        {
            'numero': 1,
            'titulo': 'El Despertar',
            'periodo_academico': '1er Periodo',
            'xp_minimo_aprobacion': 3000,
            'xp_maximo': 5000,
            'xp_tope_recuperacion': 3500
        },
        {
            'numero': 2,
            'titulo': 'La Forja',
            'periodo_academico': '2do Periodo',
            'xp_minimo_aprobacion': 3000,
            'xp_maximo': 5000,
            'xp_tope_recuperacion': 3500
        },
        {
            'numero': 3,
            'titulo': 'La Tormenta',
            'periodo_academico': '3er Periodo',
            'xp_minimo_aprobacion': 3000,
            'xp_maximo': 5000,
            'xp_tope_recuperacion': 3500
        },
        {
            'numero': 4,
            'titulo': 'El Juicio Final',
            'periodo_academico': '4to Periodo',
            'xp_minimo_aprobacion': 3000,
            'xp_maximo': 5000,
            'xp_tope_recuperacion': 3500
        }
    ]

    with app.app_context():
        for data in niveles:
            nivel = Nivel(**data)
            db.session.add(nivel)
        db.session.commit()
        print("✅ 4 mundos creados exitosamente.")

if __name__ == '__main__':
    seed_niveles()