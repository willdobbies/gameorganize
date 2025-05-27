from gameorganize.db import db
from sqlalchemy import event, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    progress_cur: Mapped[int] = mapped_column(nullable=False)
    progress_max: Mapped[int] = mapped_column(nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey("game_entry.id"))

    @validates('progress_max')
    def validate_progress_max(self, key, value):
        if value <= 0:
            raise ValueError("Progress must be above 1")
        return value

    def get_perc(self):
        if(self.progress_max == 0):
            raise ValueError("Invalid total progress value!")
        return self.progress_cur / self.progress_max
