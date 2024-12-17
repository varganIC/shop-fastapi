from typing import (
    Optional,
    Type,
    TypeVar
)

from sqlalchemy.orm.collections import InstrumentedList

T = TypeVar("T")


def validate_field_orm_relation(
    value, generic_type: Type[T], field: Optional[str] = None
):
    if not value or type(value) is not InstrumentedList:
        return value

    results = []

    for item in value:
        model_object = generic_type(**item._asdict())
        results.append(getattr(model_object, field) if field else model_object)

    return results
