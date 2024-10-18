from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    slug: str
    image_small: str
    image_small: str
    image_large: str
    subcategory_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int