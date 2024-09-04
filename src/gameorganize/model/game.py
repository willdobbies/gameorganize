from sqlalchemy.orm import Mapped, mapped_column
import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Completion(enum.Enum):
    Null = -1
    Unplayed = 0
    Started = 1
    Beaten = 2
    Completed = 3
    Endless = 4

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
    name: Mapped[str] = mapped_column(unique=True)
    platform: Mapped[str] = mapped_column()
    completion: Mapped[Completion] = mapped_column(default=Completion.Unplayed)
    ownership: Mapped[Ownership] = mapped_column(default=Ownership.Physical)
    priority: Mapped[Priority] = mapped_column(default=Priority.Normal)
    cheev: Mapped[int] = mapped_column(default=0)
    cheev_total: Mapped[int] = mapped_column(default=0)
    notes:Mapped[str] = mapped_column(default="")

    def __repr__(self):
        return f'<Game {self.name} @ {self.platform} [{self.completion.name}]>'

def test_entries():
    # Add some games
    g1 = GameEntry(
        name="Oddworld: Abe's Oddysee", 
        platform="PC", 
        completion=Completion.Beaten, 
        ownership=Ownership.Digital, 
        priority=Priority.Normal, 
        notes="I really liked this game",
    )

    g2 = GameEntry(
        name="Pikmin 2", 
        platform="GameCube", 
        completion=Completion.Started, 
        priority=Priority.Low, 
    )

    g3 = GameEntry(
        name="Kingdom Hearts", 
        platform="PS2", 
        completion=Completion.Completed, 
        priority=Priority.Replay, 
        cheev=100, 
        cheev_total=100
    )

    #session.add(g1)
    #session.add(g2)
    #session.add(g3)
    #session.commit()