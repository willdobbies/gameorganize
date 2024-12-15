from gameorganize.db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[int] = mapped_column()