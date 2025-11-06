"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings configuration"""
    
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
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
    secret_key: str = "your-secret-key-here"    # TCS GenAI Lab Configuration
    genai_base_url: str = "https://genailab.tcs.in"
    genai_model: str = "azure_ai/genailab-maas-DeepSeek-V3-0324"  # Default model
    genai_api_key: Optional[str] = None
    
    # Available models for selection
    available_models: list = [
        "azure/genailab-maas-gpt-35-turbo",
        "azure/genailab-maas-gpt-4o", 
        "azure/genailab-maas-gpt-4o-mini",
        "azure_ai/genailab-maas-DeepSeek-R1",
        "azure_ai/genailab-maas-Llama-3.3-70B-Instruct",
        "azure_ai/genailab-maas-DeepSeek-V3-0324",
        "gemini-2.0-flash-001",
        "gemini-2.5-flash",
        "gemini-2.5-pro"
    ]
      # API
    api_v1_prefix: str = "/api/v1"


# Global settings instance
settings = Settings()
