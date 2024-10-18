import urllib.parse
import uuid
from ast import literal_eval
from os import environ
from typing import (
    List,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    BaseSettings,
    Field,
    validator
)
from sqlalchemy.pool import NullPool


class DBSettingsModel(BaseModel):
    host: str
    port: int
    user: str
    pwd: str
    db_name: str

    def sql_alchemy_conn_string_async(self):
        return (
            f"postgresql+asyncpg://{self.user}:{urllib.parse.quote(self.pwd)}"
            f"@{self.host}:{self.port}/{self.db_name}"
        )


class AppSettings(BaseSettings):
    db_settings: DBSettingsModel
    uvicorn_settings: dict

    @validator("uvicorn_settings", pre=True)
    def validate_uvicorn_settings(cls, value):
        if isinstance(value, str):
            value = literal_eval(value)
            for idx, item in value.items():
                value[idx] = environ.get(item, None)
                if value[idx] is not None and value[idx].isdigit():
                    value[idx] = int(value[idx])

        return value


