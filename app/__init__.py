from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

from .extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    
    # Konfigurer SQLAlchemy og Sessions
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db  # Bruk eksisterende db-instans
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    db.init_app(app)  # Initialiser db med app
    Session(app)  # Initialiser session med app


    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(app, supports_credentials=True)

    with app.app_context():
        from . import models, routes
        app.register_blueprint(routes.bp)
        db.create_all()

    return app
