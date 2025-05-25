from flask_login import UserMixin
from gameorganize.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from .game import GameEntry
from .platform import Platform
import re
from werkzeug.security import generate_password_hash

rex_password = re.compile("^(?=.*?[A-Z])(?=.*?[a-z]).{8,}$")

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[int] = mapped_column()
    games = relationship('GameEntry', backref='user')
    platforms = relationship('Platform', backref='user')

    @validates('username')
    def validate_username(self,key,value):
        if(not value):
            raise ValueError("Username must not be empty")
        return value
    
    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        if(not rex_password.match(password)):
            raise ValueError("Password must be at least 8 characters long and contain an uppercase letter")
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha1')