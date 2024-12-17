from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    slug: str
    image_small: str
    image_medium: str
    image_large: str
    price: int
    subcategory_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int


class ProductComposite(BaseModel):
    id: int
    name: str
    slug: str
    image_small: str
    image_medium: str
    image_large: str
    price: int
    subcategory: str
    category: str
