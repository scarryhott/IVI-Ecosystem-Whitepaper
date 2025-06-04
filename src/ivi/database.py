from __future__ import annotations

"""Simple SQLAlchemy models for persistence."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    idea_id = Column(String, nullable=False)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

def create_db(url: str = "sqlite:///:memory:") -> sessionmaker:
    """Create tables and return a session factory."""
    engine = create_engine(url, future=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True)
