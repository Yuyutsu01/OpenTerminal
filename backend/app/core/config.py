import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # API configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Indian Economic Intelligence Platform"
    
    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # LLM API Keys (optional, with fallback support)
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    
    # Environment config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings singleton
settings = Settings()
