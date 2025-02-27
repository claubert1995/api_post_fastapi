from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str 
    DEBUG: bool = False
    TESTING: bool = False
    DATABASE_URL: str 
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()