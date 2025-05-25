from gameorganize.model.game import GameEntry, Completion, Priority, Ownership
from gameorganize.model.platform import Platform
from gameorganize.model.user import User
import pytest

def setup_db(db_session):
    new_user = User(
        username="user",
        password="PassWord",
    )
    db_session.add(new_user)
    db_session.commit()

    new_platform = Platform(
        name="Playstation",
        user_id = new_user.id,
    )
    db_session.add(new_platform)
    db_session.commit()

    new_game_entry = GameEntry(
        name="Spyro The Dragon",
        user_id = new_user.id,
        platform_id = new_platform.id,
    )
    db_session.add(new_game_entry)
    db_session.commit()

def test_game_entry(db_session):
    setup_db(db_session)

    search_user = db_session.query(User).filter_by(username="user").first()

    search_platform = db_session.query(Platform).filter_by(name="Playstation").first()
    assert (search_platform.user_id == search_user.id)

    search_game = db_session.query(GameEntry).filter_by(name="Spyro The Dragon").first()
    assert (search_game.user_id == search_user.id)
    assert (search_game.platform_id == search_platform.id)

def test_delete_platform(db_session):
    setup_db(db_session)

    search_platform = db_session.query(Platform).filter_by(name="Playstation").first()
    search_game = db_session.query(GameEntry).filter_by(platform_id=search_platform.id).first()

    db_session.delete(search_platform)
    db_session.commit()

    assert (search_game.platform_id == None)
