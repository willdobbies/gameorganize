from flask import Flask
from .db import db
from .config import DevelopmentConfig

def create_app(config = DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    register_blueprints(app)
    init_extensions(app)

    with app.app_context():
        db.create_all()
        return app

def register_blueprints(app):
    from .game import game
    from .gamelist import gamelist
    from .importer import importer
    from .platform import platform

    app.register_blueprint(game, url_prefix='/game')
    app.register_blueprint(gamelist)
    app.register_blueprint(importer, url_prefix='/import')
    app.register_blueprint(platform, url_prefix='/platform')

def init_extensions(app):
    db.init_app(app)