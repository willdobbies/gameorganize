from db import db
from flask import Flask
from game import game
from gamelist import gamelist
from importer import importer

app = Flask(__name__)
app.config['SECRET_KEY'] = '7103fd2f0697987fef0626de455aeb8617f8318c2ecaad41'
app.config['MAX_CONTENT_PATH'] = pow(10,7)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.sqlite3"
app.config['UPLOAD_FOLDER'] = "./instance/"

# Add blueprint modules
app.register_blueprint(game, url_prefix='/game')
app.register_blueprint(gamelist)
app.register_blueprint(importer, url_prefix='/import')

# setup sqlalchemy
db.init_app(app)

# Create the database tables and start app
with app.app_context():
  db.create_all()