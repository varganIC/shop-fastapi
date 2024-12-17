from sqlalchemy import (
    Column,
    ForeignKey,
    Integer
)
from sqlalchemy.sql import expression

from common.helpers import decorator
from db.models.common import Base


@decorator("_asdict")
class Bucket(Base):
    __tablename__ = 'bucket'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    product_id = Column(
        Integer,
        ForeignKey('product.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    quantity = Column(
        Integer,
        nullable=False,
        server_default=expression.literal(1)
    )
