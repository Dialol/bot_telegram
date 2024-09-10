from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import Set


class Settings(BaseSettings):
    bot_token: SecretStr
    OPERATORS: Set[int] = {186060158}

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


config = Settings()
