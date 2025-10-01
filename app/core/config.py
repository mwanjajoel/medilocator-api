import os
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    api_version: str = "1.0.0"
    project_name: str = "Medilocator API"
    
    # Security
    jwt_secret: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_days: int = 30
    
    # Supabase
    supabase_url: str
    supabase_key: str
    
    # OpenAI
    openai_api_key: str
    
    # CORS
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()