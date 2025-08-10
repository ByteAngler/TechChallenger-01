from functools import lru_cache
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    csv_path: str = "data/books.csv"

@lru_cache
def get_settings():
    return Settings()
