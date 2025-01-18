
from flask import Flask
from flask_cors import CORS
from config import Config

from .routes.user_bp import users_bp
from .routes.socios_bp import socios_bp
from .routes.cuotas_bp import cuotas_bp
from .routes.actividades_bp import actividades_bp
from .routes.auth_bp import auth_bp
from .database import DatabaseConnection

def init_app():
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
    
    CORS(app, supports_credentials=True)

    app.config.from_object(Config)

    DatabaseConnection.set_config(app.config)

    app.register_blueprint(socios_bp, url_prefix='/socios')
    app.register_blueprint(cuotas_bp, url_prefix='/cuotas')
    app.register_blueprint(actividades_bp, url_prefix='/actividades')
    app.register_blueprint(auth_bp, url_prefix = '/auth')
    app.register_blueprint(users_bp, url_prefix = '/user')

    return app
