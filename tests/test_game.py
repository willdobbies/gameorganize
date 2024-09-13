from model.game import GameEntry, Completion, Priority, Ownership

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

    assert(g1 is not None)
    assert(g2 is not None)
    assert(g3 is not None)