"""
Ponto de entrada da aplicação FastAPI.

Responsabilidades:
- Configurar e inicializar a aplicação.
- Carregar o CSV em memória na inicialização (app.state.df).
- Configurar o lock global para evitar scraping concorrente.
- Registrar os routers versionados (v1).
- Redirecionar "/" para o healthcheck.
"""
from fastapi import FastAPI
from app.api.v1.endpoints import books, categories, health, scraping
from fastapi.responses import RedirectResponse
import pandas as pd
from app.core.config import get_settings
from threading import Lock

app = FastAPI(title="Book API", version="1.0.0")
settings = get_settings()

@app.on_event("startup")
def load_data():
    """
    Evento de inicialização da API.

    - Cria um Lock em app.state.scrape_lock para impedir execuções simultâneas do scraper.
    - Lê o CSV do caminho definido em Settings e guarda em app.state.df.
    - Garante a existência da coluna 'id' e normaliza tipos para nativos Python
      (evita problemas de serialização com numpy.int64 etc.).
    """
    app.state.scrape_lock = Lock()
    app.state.csv_path = settings.csv_path
    try:
        df = pd.read_csv(settings.csv_path)
        if "id" not in df.columns:
            df = df.reset_index().rename(columns={"index": "id"})
        for col, cast in (("id", int), ("rating", int), ("price", float)):
            if col in df.columns:
                df[col] = df[col].apply(lambda x: None if pd.isna(x) else cast(x))
        app.state.df = df
    except FileNotFoundError:
        app.state.df = None

@app.get("/")
def home():
    return RedirectResponse(url="/api/v1/health")

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(books.router,  prefix="/api/v1", tags=["Books"])
app.include_router(categories.router, prefix="/api/v1", tags=["Categories"])
app.include_router(scraping.router,   prefix="/api/v1", tags=["Scraping"])