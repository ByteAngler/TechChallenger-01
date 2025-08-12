"""
Configurações centralizadas da aplicação.

- Usa pydantic-settings para permitir leitura via variáveis de ambiente.
- Ex.: CSV_PATH=/app/data/books.csv
"""
from functools import lru_cache
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    """
    Define as configurações do app.

    Attributes:
        csv_path: Caminho do arquivo CSV de dados.
    """
    csv_path: str = "data/books.csv"

@lru_cache
def get_settings():
    """
    Retorna uma instância cacheada de Settings (singleton).

    Returns:
        Settings: Instância de configurações.
    """
    return Settings()
