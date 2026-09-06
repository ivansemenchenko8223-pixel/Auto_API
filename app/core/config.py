from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./detal.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


config = Config()
