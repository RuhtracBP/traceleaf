from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TRACELEAF_", env_file=".env", extra="ignore", hide_input_in_errors=True
    )

    database_url: SecretStr
    redis_url: SecretStr
    model_api_key: SecretStr | None = None
    allowed_hosts: list[str] = ["localhost", "127.0.0.1", "api", "testserver"]
