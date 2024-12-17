from gameorganize.db import db
from sqlalchemy import event, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Platform(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    games = relationship('GameEntry', backref='platform')

    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='platform_unique_constraint'),
    )

def get_user_platforms(user_id:int):
    return db.session.query(Platform).where(Platform.user_id==user_id).order_by(Platform.name)

def find_platform(name:str):
    return db.session.query(Platform).where(Platform.name==name).first()

#@event.listens_for(Platform.__table__, 'after_create')
#def platform_after_create(target, connection, **kw):
#    print("Prefilling Platform values")
#    default_names = [
#        'Arcade',
#        'Neo Geo',
#        'Nintendo 3DS',
#        'Nintendo 64',
#        'Nintendo DS',
#        'Nintendo Entertainment System',
#        'Nintendo GameCube',
#        'Nintendo Gameboy Advance', 
#        'Nintendo Gameboy', 
#        'Nintendo SNES', 
#        'Nintendo Switch',
#        'PC',
#        'Playstation 2',
#        'Playstation 3',
#        'Playstation 4',
#        'Playstation',
#        'Scumm VM',
#        'Sega Dreamcast', 
#        'Sega Genesis', 
#        'Sega Saturn', 
#        'Xbox 360', 
#        'Xbox One', 
#        'Xbox', 
#    ]
#
#    for name in default_names:
#        db.session.add(Platform(name=name))
#    db.session.commit()