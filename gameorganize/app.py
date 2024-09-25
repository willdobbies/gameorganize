from .db import db
from .game import game
from .gamelist import gamelist
from .importer import importer
from .platform import platform
from flask import Flask
from flask_migrate import Migrate
from .config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Add blueprint modules
app.register_blueprint(game, url_prefix='/game')
app.register_blueprint(gamelist)
app.register_blueprint(importer, url_prefix='/import')
app.register_blueprint(platform, url_prefix='/platform')

# setup sqlalchemy
db.init_app(app)

# setup migrations
migrate = Migrate(app, db)

# Create the database tables and start app
with app.app_context():
  db.create_all()
