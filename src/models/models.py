from src.db.database import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
import uuid


class User(Base):
    __tablename__ = "app_user"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()"))
    username = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)

    film_statuses = relationship("FilmStatus", back_populates="user")


class Film(Base):
    __tablename__ = "film"

    id = Column(Integer, primary_key=True, nullable=False)
    score = Column(Numeric(3, 1), nullable=False, server_default=text("0"))

    statuses = relationship("FilmStatus", back_populates="film")
    genres = relationship("Genre", secondary="film_genres", back_populates="films")


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(30), nullable=False)

    films = relationship("Film", secondary="film_genres", back_populates="genres")


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)


class FilmGenres(Base):
    __tablename__ = "film_genres"

    genre_id = Column(Integer, ForeignKey("genre.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)
    film_id = Column(Integer, ForeignKey("film.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)


class FilmStatus(Base):
    __tablename__ = "film_status"

    user_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True, server_default=text("gen_random_uuid()"))
    film_id = Column(Integer, ForeignKey("film.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)
    status_id = Column(Integer, ForeignKey("status.id", ondelete="NO ACTION", onupdate="NO ACTION"))
    user_score = Column(Numeric(3, 1))

    user = relationship("User", back_populates="film_statuses")
    film = relationship("Film", back_populates="statuses")
