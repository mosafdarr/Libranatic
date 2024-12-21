from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME", default="Integration Repo")
    DATABASE_URL: str = Field(env="DATABASE_URL", default="postgresql://postgres:mosafdar%%40123@localhost:5432/integrationdb")
    DATABASE_ENGINE_ECHO: bool = Field(env="DATABASE_ENGINE_ECHO", default=True) # set to false in production
    
    # JWT Configuration
    SECRET_KEY: str = Field(env="SECRET_KEY", default="your-secret-key")
    ALGORITHM: str = Field(env="ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(env="ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
    
    # Logging
    LOG_LEVEL: str = Field(env="LOG_LEVEL", default="INFO")
    
    # Security
    CORS_ORIGINS: list[str] = Field(env="CORS_ORIGINS", default=["*"])
    
    # Additional Environment-specific settings
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra='ignore'
    )

settings = Settings()
