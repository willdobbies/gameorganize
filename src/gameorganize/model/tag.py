from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Tag(Base):
    __tablename__ = "tags"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String)