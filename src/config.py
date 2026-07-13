"""统一配置入口。

用 pydantic-settings 从 `.env` / 环境变量加载配置,供 DB / Redis / DeepSeek
客户端复用。字段名小写,pydantic-settings 会自动大小写不敏感匹配环境变量
(如 DATABASE_URL → database_url)。
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://memory:memory_dev@localhost:5432/memory_service"
    redis_url: str = "redis://localhost:6379/0"

    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"


settings = Settings()
