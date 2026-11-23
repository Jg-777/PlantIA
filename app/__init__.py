from pathlib import Path

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.shared.database import db, migrate
from app.shared.exceptions import AppException

# Importar modelos para que SQLAlchemy y Flask-Migrate los reconozcan
from app.domains.auth import models as auth_models
from app.domains.diagnostico import models as diagnostico_models
from app.domains.inventario import models as inventario_models
from app.domains.ventas import models as ventas_models

# Importar controladores
from app.domains.auth.controllers import auth_bp
from app.domains.diagnostico.controllers import diagnostico_bp
from app.domains.inventario.controllers import inventario_bp
from app.domains.ventas.controllers import ventas_bp


# Ubicación del HTML principal
FRONTEND_TEMPLATES = (
    Path(__file__).resolve().parent.parent / "render_template"
)


def create_app(config_class=Config):

    app = Flask(
        __name__,
        template_folder=str(FRONTEND_TEMPLATES)
    )

    # Configuración
    app.config.from_object(config_class)

    # Configuración CORS
    CORS(app)

    # Inicializar base de datos y migraciones
    db.init_app(app)
    migrate.init_app(app, db)

    # Página principal
    @app.get("/")
    def index():
        return render_template("PlantIA_Profesional.html")

    # Registrar rutas de la API
    app.register_blueprint(auth_bp)
    app.register_blueprint(diagnostico_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(ventas_bp)

    # Manejo de errores personalizados
    @app.errorhandler(AppException)
    def handle_app_exception(err):
        status_code = getattr(err, "status_code", 400)
        error_code = getattr(err, "error_code", getattr(err, "code", "APP_ERROR"))
        message = getattr(err, "message", str(err))
        details = getattr(err, "details", None)

        response = {
            "success": False,
            "error": message,
            "code": error_code,
        }

        if details is not None:
            response["details"] = details

        return jsonify(response), status_code

    # Manejo de errores HTTP estándar (ej. 404 /favicon.ico)
    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        return jsonify({
            "success": False,
            "error": err.description,
            "code": f"HTTP_{err.code}",
        }), err.code

    # Manejo de errores inesperados
    @app.errorhandler(Exception)
    def handle_unexpected_exception(err):

        app.logger.exception("Error inesperado")

        return jsonify({
            "success": False,
            "error": "Error interno del servidor.",
            "code": "INTERNAL_SERVER_ERROR"
        }), 500

    return app