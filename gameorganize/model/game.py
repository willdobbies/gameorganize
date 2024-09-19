from gameorganize.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from gameorganize.model.platform import Platform

class Completion(enum.Enum):
    Null = -1
    Unplayed = 0
    Started = 1
    Beaten = 2
    Completed = 3
    Endless = 4

    def get_color(self):
        if (self == self.Unplayed):
            return 'primary'
        elif (self == self.Started):
            return 'danger'
        elif (self == self.Beaten):
            return 'success'
        elif (self == self.Completed):
            return 'warning'
        elif (self == self.Endless):
            return 'secondary'
        return "secondary"

class Ownership(enum.Enum):
    Physical = 0
    Digital = 1
    FormerlyOwned = 2
    Subscription = 3
    Wishlist = 4

class Priority(enum.Enum):
    Abandoned = -1
    Paused = 1
    Low = 2
    Normal = 3
    High = 4
    NowPlaying = 5
    Replay = 6

class GameEntry(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    #platform: Mapped[str] = mapped_column()
    platform_id: Mapped[int] = mapped_column(ForeignKey("platform.id"), nullable=True) 
    platform = relationship(Platform, foreign_keys=[platform_id])
    completion: Mapped[Completion] = mapped_column(default=Completion.Unplayed)
    ownership: Mapped[Ownership] = mapped_column(default=Ownership.Physical)
    priority: Mapped[Priority] = mapped_column(default=Priority.Normal)
    cheev: Mapped[int] = mapped_column(default=0)
    cheev_total: Mapped[int] = mapped_column(default=0)
    notes:Mapped[str] = mapped_column(default="")

    def __repr__(self):
        return f'<Game {self.name} @ {self.platform} [{self.completion.name}]>'
