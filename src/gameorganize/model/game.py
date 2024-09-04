from sqlalchemy.orm import sessionmaker 
import sqlalchemy as sa
import enum

Base = sa.orm.declarative_base()

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

class GameEntry(Base):
    __tablename__ = "game_entry"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String)
    platform = sa.Column("platform", sa.String)
    completion = sa.Column(sa.Enum(Completion), default=Completion.Unplayed)
    ownership = sa.Column(sa.Enum(Ownership), default=Ownership.Physical)
    priority = sa.Column(sa.Enum(Priority), default=Priority.Normal)
    cheev = sa.Column("cheev", sa.Integer, default=0)
    cheev_total = sa.Column("cheev_total", sa.Integer, default=0)
    notes = sa.Column("notes", sa.String, default="")

    def __repr__(self):
        return f'<Game {self.name} @ {self.platform} [{self.completion.name}]>'

if (__name__ == "__main__"):
    engine = sa.create_engine("sqlite:///games.sqlite3", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session() 

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

    session.add(g1)
    session.add(g2)
    session.add(g3)
    session.commit()