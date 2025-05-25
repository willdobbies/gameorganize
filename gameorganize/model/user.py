from flask_login import UserMixin
from gameorganize.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .game import GameEntry
from .platform import Platform

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[int] = mapped_column()
    games = relationship('GameEntry', backref='user')
    platforms = relationship('Platform', backref='user')