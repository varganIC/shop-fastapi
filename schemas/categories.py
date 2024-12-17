from typing import List, Optional

from pydantic import (
    BaseModel,
    Field,
    validator
)

from schemas.common import validate_field_orm_relation


class CategoryBase(BaseModel):
    name: str
    slug: str
    image: str


class CategoryCreate(CategoryBase):
    name: Optional[str]
    slug: Optional[str]
    image: Optional[str]


class Category(CategoryBase):
    id: int


class SubCategoryBase(BaseModel):
    name: str
    slug: str
    image: str
    category_id: int


class SubCategoryCreate(SubCategoryBase):
    name: Optional[str]
    slug: Optional[str]
    image: Optional[str]
    category_id: Optional[int]


class SubCategory(SubCategoryBase):
    id: int


class CategoryComposite(Category):
    subcategories: Optional[List[SubCategory]] = Field(
        description="Список подкатегорий",
        title="Список подкатегорий",
        # alias='links',
    )

    @validator("subcategories", pre=True, check_fields=False)
    def set_links(cls, v):
        return validate_field_orm_relation(v, SubCategory)
