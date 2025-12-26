import pathlib
import typing

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict


class DatabaseSettings(BaseSettings):
    URL: PostgresDsn = Field()

    @field_validator("URL")
    def check_db_name(cls, v: PostgresDsn) -> PostgresDsn:
        if (not v.path) or len(v.path) <= 1:
            raise ValueError("database must be provided")
        return v


def convert_umask_to_int(value: int) -> int:
    return int(str(value), 8)


class WikiSettings(BaseSettings):
    NAME: str = Field(
        default="Cicada26",
        description="The name of your wiki. Defaults to the application's name, Cicada26.",
    )
    STORE: pathlib.Path = Field(
        description="The path to your wiki, where its content will be stored."
    )


class Settings(BaseSettings):
    model_config: typing.ClassVar[SettingsConfigDict] = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="C26_",
        env_file=("../../.env", ".env"),
        # env_file=(pathlib.Path("../../.env").resolve(), ".env"),
        env_nested_delimiter="_",
        env_nested_max_split=1,
        extra="ignore",
    )

    WIKI: WikiSettings
    # DB: DatabaseSettings


settings: Settings = Settings()  # pyright: ignore[reportCallIssue]  # ty: ignore[missing-argument]
