from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Integration Repo"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Security
    CORS_ORIGINS: list[str] = ["*"]
    
    # Additional Environment-specific settings
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra='ignore'
    )

settings = Settings()