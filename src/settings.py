import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME", default="Linranatic")
    DATABASE_URL: str = Field(env="DATABASE_URL", default="postgresql://postgres:mosafdar123@localhost:5432/libranatic")
    DATABASE_ENGINE_ECHO: bool = Field(env="DATABASE_ENGINE_ECHO", default=True) # set to false in production
    TIMEOUT: int = Field(env="TIMEOUT", default=30)

    # LLamma Configuration
    LLAMA_API_KEY: str = Field(env="LLAMA_API_KEY", default=os.getenv("LLAMA_API_KEY"))
    LLAMA_MODEL_NAME: str = Field(env="LLAMA_MODEL_NAME", default="llama3-8b-8192")

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

class DatabaseConfig(BaseSettings):
    @classmethod
    def get_session(cls):
        from schema.database import get_session
        with get_session() as session:
            yield session

settings = Settings()
db_config = DatabaseConfig()
