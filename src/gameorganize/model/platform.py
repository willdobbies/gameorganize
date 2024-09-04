from gameorganize.model.db import db
from sqlalchemy.orm import Mapped, mapped_column

class Platform(db.Model):
    __tablename__ = "platforms"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(primary_key=True)