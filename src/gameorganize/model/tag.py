from gameorganize.model.db import db
from sqlalchemy.orm import Mapped, mapped_column

class Tag(db.Model):
    __tablename__ = "tags"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(primary_key=True)