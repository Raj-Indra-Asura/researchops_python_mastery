"""Application settings loaded from environment variables.

We use pydantic-settings so that:
- settings can come from .env files, environment variables, or defaults
- all values are type-checked at startup
- secrets are never hard-coded

Usage:
    from researchops.config.settings import settings
    print(settings.db_path)
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration.

    Values are loaded in this priority order (highest first):
    1. Actual environment variables (e.g. ``RESEARCHOPS_LOG_LEVEL=DEBUG``)
    2. Variables in a ``.env`` file in the project root
    3. The defaults defined below
    """

    model_config = SettingsConfigDict(
        env_prefix="RESEARCHOPS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Application ---
    env: str = Field(default="development", description="Runtime environment")
    log_level: str = Field(default="INFO", description="Logging level")

    # --- Database ---
    db_path: Path = Field(
        default=Path("data/researchops.db"),
        description="Path to the SQLite database file",
    )

    # --- API ---
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)

    # --- Worker ---
    worker_concurrency: int = Field(
        default=4, ge=1, le=32, description="Number of parallel worker processes"
    )

    # --- ML / Embeddings (Week 13+) ---
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Sentence-transformer model name for embeddings",
    )

    # --- RAG / LLM (Week 17+) ---
    openai_api_key: str = Field(default="", description="OpenAI API key (optional)")
    llm_model: str = Field(default="gpt-4o-mini", description="LLM model for RAG")


# Module-level singleton — import this everywhere:
#   from researchops.config.settings import settings
settings = Settings()
