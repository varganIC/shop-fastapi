from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text
)
from sqlalchemy.orm import relationship
from db.models.common import Base, decorator


@decorator("_asdict")
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, unique=True, index=True)
    slug = Column(Text, nullable=False, unique=True)
    image = Column(Text, nullable=False,)

    subcategories = relationship("Subcategory", back_populates="categories")


@decorator("_asdict")
class Subcategory(Base):
    __tablename__ = 'subcategory'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, unique=True, index=True)
    slug = Column(Text, nullable=False, unique=True)
    image = Column(Text, nullable=False)
    category_id = Column(
        Integer,
        ForeignKey("category.id", ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    categories = relationship("Category", back_populates="subcategories")
    products = relationship("Product", back_populates="subcategories")
