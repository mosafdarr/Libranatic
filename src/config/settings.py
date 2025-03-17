from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Libranatic"
    
    class Config:
        case_sensitive = True

settings = Settings() 