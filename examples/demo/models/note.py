from sqlalchemy import Column, Integer, String, Table, Boolean
from .base import Model, metadata


class Note(Model):
    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    num = Column(Integer)


class User(Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    aeg = Column(Integer)


tests = Table(
    "tests",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String),
    Column("completed", Boolean),
)
