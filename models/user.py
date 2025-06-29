from db.database import Base
from sqlalchemy import *


class User(Base):
    __tablename__ = "app_user"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()"))
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)