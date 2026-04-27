from functools import lru_cache
from typing import Dict

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    database_url: str = Field(..., alias="DATABASE_URL")
    api_keys: str = Field(..., alias="API_KEYS")
    api_key_header: str = Field("X-API-Key", alias="API_KEY_HEADER")

    @property
    def api_key_map(self) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        entries = [entry.strip() for entry in self.api_keys.split(",") if entry.strip()]
        for entry in entries:
            if ":" not in entry:
                continue
            username, key = entry.split(":", 1)
            mapping[username.strip()] = key.strip()
        return mapping

    @property
    def key_to_user(self) -> Dict[str, str]:
        return {key: username for username, key in self.api_key_map.items()}


@lru_cache
def get_settings() -> Settings:
    return Settings()
