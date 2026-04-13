from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "1234"
    DB_NAME: str = "db"

    SECRET_KEY: str = "aslam"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # File storage settings
    FILE_STORAGE_PATH: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 5

    class Config:
        env_file = ".env"


settings = Settings()