from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # API Settings
    api_version: str = "1.0.0"
    project_name: str = "Medilocator API"

    # Security
    jwt_secret: str
    algorithm: str = "HS256"
    access_token_expire_days: int = 30

    # Supabase
    supabase_url: str
    supabase_key: str

    # OpenAI
    openai_api_key: str

    # CORS
    cors_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False

# Create the settings instance
settings = Settings()

# Ensure required environment variables are set
if not settings.supabase_url:
    raise ValueError("SUPABASE_URL environment variable is required")

if not settings.supabase_key:
    raise ValueError("SUPABASE_KEY environment variable is required")

if not settings.openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

if not settings.jwt_secret:
    raise ValueError("JWT_SECRET environment variable is required")