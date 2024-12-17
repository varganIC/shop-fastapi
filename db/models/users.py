from sqlalchemy import (
    Column,
    Integer,
    Text
)

from common.helpers import decorator
from db.models.common import Base


@decorator("_asdict")
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, nullable=False, unique=True, index=True)
    hashed_password = Column(Text, nullable=False)
