import os 

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))

def get_db_path(name):
    #return "sqlite:///" + os.path.join(basedir, f'{name}.db')
    return f"sqlite:///{name}"

# Default settings
class Config:
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = '7103fd2f0697987fef0626de455aeb8617f8318c2ecaad41'

class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_db_path("dev.sqlite3")

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = get_db_path("")

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = get_db_path("production.sqlite3")
