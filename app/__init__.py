from flask import Flask
from flask_cors import CORS
from flask_session import Session

from .extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.config['SESSION_TYPE'] = 'filesystem'


    CORS(app,supports_credentials=True)
    Session(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        from . import models, routes
        app.register_blueprint(routes.bp)
        db.create_all()

    return app
