from flask import Flask
from .db import db
from .config import DevelopmentConfig
from flask_login import LoginManager

def create_app(config = DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    register_blueprints(app)
    init_extensions(app)

    with app.app_context():
        db.create_all()
        return app

def register_blueprints(app):
    from .auth import auth
    from .game import game
    from .gamelist import gamelist
    #from .importer import importer
    from .platform import platform

    app.register_blueprint(auth)
    app.register_blueprint(game, url_prefix='/game')
    app.register_blueprint(gamelist)
    #app.register_blueprint(importer, url_prefix='/import')
    app.register_blueprint(platform, url_prefix='/platform')

def init_extensions(app):
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from gameorganize.model.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))