from gameorganize.model.game import GameEntry, Completion, Priority, Ownership
from gameorganize.model.platform import Platform
from gameorganize.model.user import User

def test_game_entry(db_session):
    # make some entries
    valid_user = User(
        id = 0,
        username="user",
        password="password",
    )
    valid_platform = Platform(
        id = 0,
        name="Playstation",
        user_id = valid_user.id,
    )
    valid_game_entry = GameEntry(
        name="Spyro The Dragon",
        user_id = valid_user.id,
        platform_id = valid_platform.id,
    )

    db_session.add(valid_user)
    db_session.add(valid_platform)
    db_session.add(valid_game_entry)
    db_session.commit()

    search_user = db_session.query(User).filter_by(username="user").first()
    assert (search_user.username == "user")
    assert (search_user.password == "password")

    search_platform = db_session.query(Platform).filter_by(name="Playstation").first()
    assert (search_platform.user_id == valid_user.id)

    search_game = db_session.query(GameEntry).filter_by(user_id=valid_user.id).first()
    assert (search_game.platform_id == search_platform.id)

def test_delete_platform(db_session):
    # make some entries
    valid_user = User(
        id = 0,
        username="user",
        password="password",
    )
    valid_platform = Platform(
        id = 0,
        name="Playstation",
        user_id = valid_user.id,
    )
    valid_game_entry = GameEntry(
        name="Spyro The Dragon",
        user_id = valid_user.id,
        platform_id = valid_platform.id,
    )

    db_session.add(valid_user)
    db_session.add(valid_platform)
    db_session.add(valid_game_entry)
    db_session.commit()

    search_platform = db_session.query(Platform).filter_by(name="Playstation").first()
    assert (search_platform.user_id == valid_user.id)

    search_game = db_session.query(GameEntry).filter_by(user_id=valid_user.id).first()
    assert (search_game.platform_id == valid_platform.id)

    db_session.delete(valid_platform)
    db_session.commit()

    assert (search_game.platform_id == None)