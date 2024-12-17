from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    Text
)
from sqlalchemy.orm import relationship

from common.helpers import decorator
from db.models.common import Base


@decorator("_asdict")
class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, index=True)
    slug = Column(Text, nullable=False, unique=True, index=True)
    price = Column(Float, nullable=False)
    image_small = Column(Text, nullable=False)
    image_medium = Column(Text, nullable=False)
    image_large = Column(Text, nullable=False)
    subcategory_id = Column(
        Integer,
        ForeignKey("subcategory.id", ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    subcategories = relationship("Subcategory", back_populates="products")
