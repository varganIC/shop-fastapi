from http import HTTPStatus
from typing import (
    Generic,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar
)

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

T = TypeVar('T')


class ValidationErrorModel(BaseModel):
    class ValidationErrorDetail(BaseModel):
        loc: Optional[List[str]]
        msg: Optional[str]
        type: Optional[str]

    detail: List[ValidationErrorDetail]


class ResponseMessage(BaseModel):
    detail: str = Field(description="Описание ошибки", title="Описание ошибки")


responses_common_200_desc = 'ОК'

responses_common_get = {
    HTTPStatus.FORBIDDEN.value: {
        "model": ResponseMessage,
        "description": "Ошибка доступа",
    },
    HTTPStatus.UNPROCESSABLE_ENTITY.value: {
        "model": ValidationErrorModel,
        "description": "Ошибка валидации данных",
    },
    HTTPStatus.INTERNAL_SERVER_ERROR.value: {
        "description": "Внутрення ошибка сервера"
    },
}

responses_common_post = {
    HTTPStatus.FORBIDDEN.value: {
        "model": ResponseMessage,
        "description": "Ошибка доступа",
    },
    HTTPStatus.UNPROCESSABLE_ENTITY.value: {
        "model": ValidationErrorModel,
        "description": "Ошибка валидации данных",
    },
    HTTPStatus.INTERNAL_SERVER_ERROR.value: {
        "description": "Внутрення ошибка сервера"
    },
}

responses_common_delete = {
    HTTPStatus.CREATED.value: {
        "model": None, "description": responses_common_200_desc
    },
    HTTPStatus.FORBIDDEN.value: {
        "model": ResponseMessage,
        "description": "Ошибка доступа",
    },
    HTTPStatus.UNPROCESSABLE_ENTITY.value: {
        "model": ValidationErrorModel,
        "description": "Ошибка валидации данных",
    },
    HTTPStatus.INTERNAL_SERVER_ERROR.value: {
        "description": "Внутрення ошибка сервера"
    },
}


class BaseResponse(Generic[T]):
    def __init__(self, generic_type: Type[T]) -> None:
        self.generic_type = generic_type

    def get_typed_response_single_as_model(self, obj) -> T:
        if obj is None:
            return None

        if isinstance(obj, list):
            obj = obj[0]

        if isinstance(obj, dict):
            return self.generic_type(**obj)

        return self.generic_type(**obj._asdict())

    def get_typed_response_multi_as_model(self, objects: Iterable) -> List[T]:
        result = []

        if objects is not None:
            for obj in objects:
                result.append(self.generic_type(**obj._asdict()))

        return result

    @staticmethod
    def get_no_content_response():
        # return Response(status_code=HTTPStatus.NO_CONTENT.value)
        return JSONResponse(content=jsonable_encoder([]))
