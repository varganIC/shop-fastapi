from typing import Optional

from pydantic import BaseModel


class BucketBase(BaseModel):
    product_id: int
    quantity: Optional[int]


class BucketCreate(BucketBase):
    pass


class Bucket(BucketBase):
    id: int


class BucketAdd(BaseModel):
    product_id: int


class BucketComposition(BaseModel):
    count: int
    amount_cost: float
