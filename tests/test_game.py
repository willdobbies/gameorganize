from gameorganize.model.game import GameEntry, Completion, Priority, Ownership
from gameorganize.model.platform import Platform
from gameorganize.db import db

def test_entries(app):
    """Add some test games, check if they go into the DB okay"""

    p1 = Platform(
        name="TestPlatform",
    )

    g1 = GameEntry(
        name="Oddworld: Abe's Oddysee", 
        platform=p1,
        completion=Completion.Beaten, 
        ownership=Ownership.Digital, 
        priority=Priority.Normal, 
        notes="I really liked this game",
    )

    g2 = GameEntry(
        name="Pikmin 2", 
        platform=p1,
        completion=Completion.Started, 
        priority=Priority.Low, 
    )

    g3 = GameEntry(
        name="Kingdom Hearts", 
        platform=p1,
        completion=Completion.Completed, 
        priority=Priority.Replay, 
        cheev=100, 
        cheev_total=100
    )

    with app.app_context():
        db.session.add(p1)
        db.session.add(g1)
        db.session.add(g2)
        db.session.add(g3)
        db.session.commit()

        games=db.session.query(GameEntry)

        assert(g1 in games)
        assert(g2 in games)
        assert(g3 in games)

        db.session.delete(p1)
        db.session.commit()

        pikmin=db.session.query(GameEntry).where(GameEntry.name == "Pikmin 2").first()
        assert(pikmin.platform is None)