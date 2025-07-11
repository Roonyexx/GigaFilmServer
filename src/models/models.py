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
    vote_average = Column(Numeric(3, 1), nullable=False, server_default=text("0"))
    original_title = Column(Text, nullable=False)
    overview = Column(Text)
    popularity = Column(Numeric)
    poster_path = Column(Text)
    release_date = Column(Date, nullable=False)
    title = Column(Text, nullable=False)
    vote_count = Column(Integer, nullable=False, server_default=text("0"))
    budget = Column(Integer, nullable=False, server_default=text("0"))
    revenue = Column(BIGINT, nullable=False, server_default=text("0"))
    runtime = Column(Integer, nullable=False, server_default=text("0"))
    director_id = Column(Integer, ForeignKey("director.id", ondelete="RESTRICT", onupdate="RESTRICT"))

    statuses = relationship("FilmStatus", back_populates="film")
    genres = relationship("Genre", secondary="film_genre", back_populates="films")
    director = relationship("Director", back_populates="films")

    actors = relationship("Actor", secondary="film_actor", back_populates="films")


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(30), nullable=False)

    films = relationship("Film", secondary="film_genre", back_populates="genres")
    tvs = relationship("TV", secondary="tv_genre", back_populates="genres")

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)

class FilmGenre(Base):
    __tablename__ = "film_genre"

    genre_id = Column(Integer, ForeignKey("genre.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)
    film_id = Column(Integer, ForeignKey("film.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)

class FilmStatus(Base):
    __tablename__ = "film_status"

    user_score = Column(Integer)
    film_id = Column(Integer, ForeignKey("film.id", ondelete="RESTRICT", onupdate="RESTRICT"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True, server_default=text("gen_random_uuid()"))
    status_id = Column(Integer, ForeignKey("status.id", ondelete="RESTRICT", onupdate="RESTRICT"))
    id = Column(Integer, primary_key=True, autoincrement=True)
    tv_id = Column(Integer, ForeignKey("tv.id", ondelete="RESTRICT", onupdate="RESTRICT"))
    added_at = Column(TIMESTAMP, server_default=text("now()"))

    user = relationship("User", back_populates="film_statuses")
    film = relationship("Film", back_populates="statuses")

class TV(Base):
    __tablename__ = "tv"

    id = Column(Integer, primary_key=True, nullable=False)
    vote_average = Column(Numeric(3, 1), nullable=False, server_default=text("0"))
    original_name = Column(Text, nullable=False)
    overview = Column(Text)
    popularity = Column(Numeric)
    poster_path = Column(Text)
    first_air_date = Column(Date, nullable=False)
    name = Column(Text, nullable=False)
    vote_count = Column(Integer, nullable=False, server_default=text("0"))
    last_air_date = Column(Date)
    status = Column(Text)
    number_of_episodes = Column(Integer, nullable=False, server_default=text("0"))
    number_of_seasons = Column(Integer, nullable=False, server_default=text("0"))

    genres = relationship("Genre", secondary="tv_genre", back_populates="tvs")
    actors = relationship("Actor", secondary="tv_actor", back_populates="tvs")


class TVGenre(Base):
    __tablename__ = "tv_genre"

    genre_id = Column(Integer, ForeignKey("genre.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)
    tv_id = Column(Integer, ForeignKey("tv.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)

class Actor(Base):
    __tablename__ = "actor"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    character = Column(Text)

    films = relationship("Film", secondary="film_actor", back_populates="actors")
    tvs = relationship("TV", secondary="tv_actor", back_populates="actors")

class FilmActor(Base):
    __tablename__ = "film_actor"

    actor_id = Column(Integer, ForeignKey("actor.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)
    film_id = Column(Integer, ForeignKey("film.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)

class TVActor(Base):
    __tablename__ = "tv_actor"

    actor_id = Column(Integer, ForeignKey("actor.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)
    tv_id = Column(Integer, ForeignKey("tv.id", ondelete="CASCADE", onupdate="RESTRICT"), primary_key=True)

class Director(Base):
    __tablename__ = "director"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)

    films = relationship("Film", back_populates="director")