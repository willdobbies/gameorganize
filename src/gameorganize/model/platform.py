from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Platform(Base):
    __tablename__ = "platforms"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String)