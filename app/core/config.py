"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings configuration"""
    
    # Application
    app_name: str = "Hemanth's FastAPI Application"
    app_version: str = "1.0.0"
    description: str = "A professional FastAPI application with clean architecture"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # Security
    secret_key: str = "your-secret-key-here"
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


# Global settings instance
settings = Settings()
