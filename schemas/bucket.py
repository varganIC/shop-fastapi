from pydantic import BaseModel


class BucketBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class BucketCreate(BucketBase):
    pass


class Bucket(BucketBase):
    id: int
