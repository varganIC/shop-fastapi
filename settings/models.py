import urllib.parse
from ast import literal_eval
from os import environ

from pydantic import (
    BaseModel,
    BaseSettings,
    validator
)


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


class TokenSettings(BaseModel):
    secret_key: str
    algorithm: str
    access_exp_minutes: int


class AppSettings(BaseSettings):
    db_settings: DBSettingsModel
    token_settings: TokenSettings
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
