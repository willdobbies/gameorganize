from flask import Flask, render_template, redirect, url_for
from .db import db
from .config import DevelopmentConfig
from flask_login import LoginManager, current_user

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
    from .user import user
    from .platforms import platforms
    from .importer import importer

    @app.errorhandler(404) 
    def not_found(e): 
        return render_template("404.html") 

    @app.route("/", methods=['GET'])
    def home():
        if(current_user.is_authenticated):
            return redirect(url_for('user.detail', username=current_user.username))
        return render_template("home.html")

    app.register_blueprint(auth)
    app.register_blueprint(game, url_prefix="/game/")
    app.register_blueprint(user, url_prefix="/user/<username>")
    app.register_blueprint(platforms, url_prefix="/platforms")
    app.register_blueprint(importer, url_prefix='/import')

def init_extensions(app):
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'home'
    login_manager.init_app(app)

    from gameorganize.model.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))