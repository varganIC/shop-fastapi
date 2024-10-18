from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    slug: str
    image: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int


class SubcategoryBase(BaseModel):
    name: str
    slug: str
    image: str
    category_id: int


class SubcategoryCreate(SubcategoryBase):
    pass


class Subcategory(SubcategoryBase):
    id: int