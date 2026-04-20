import os

from flask import Flask, jsonify, redirect, url_for
from backend.config import Config
from backend.extensions import db, migrate
from routes.admin import admin_bp
from routes.public import public_bp
import models


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return redirect(url_for("admin.dashboard"))

    @app.route("/health")
    def health_check():
        return jsonify({
            "status": "ok",
            "message": "Hola, NIVEX está vivo"
        })

    return app


app = create_app()


if __name__ == "__main__":
    is_production = os.environ.get("RENDER", False) or os.environ.get("DYNO", False)
    port = int(os.environ.get("PORT", 5000))
    debug = not is_production

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not debug:
        print("=" * 60)
        print("NIVEX - PANEL ADMINISTRATIVO")
        print("=" * 60)
        print(f"Puerto: {port}")
        print(f"Modo: {'Producción' if is_production else 'Desarrollo'}")
        print(f"Debug: {'Activado' if debug else 'Desactivado'}")
        print("Inicio por defecto: http://127.0.0.1:5000/admin/dashboard")
        print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug
    )