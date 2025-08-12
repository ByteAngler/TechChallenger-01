"""
Endpoints relacionados ao processo de scraping/atualização de dados.

- POST /scraping/trigger: dispara o scraping em background e recarrega o DF.
- Garante execução única por vez usando um Lock global (app.state.scrape_lock).
"""
from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from threading import Lock
import pandas as pd

from app.services import scraper

router = APIRouter()

def _reload_dataframe(app) -> None:
    """
    Recarrega o CSV em memória (app.state.df) após o scraping.

    Args:
        app: Instância FastAPI (request.app) para acessar o state.
    """

    csv_path = getattr(app.state, "csv_path", "data/books.csv")
    df = pd.read_csv(csv_path)

    if "id" not in df.columns:
        df = df.reset_index().rename(columns={"index": "id"})

    for col, cast in (("id", int), ("rating", int), ("price", float)):
        if col in df.columns:
            df[col] = df[col].apply(lambda x: None if pd.isna(x) else cast(x))

    app.state.df = df

def _scrape_and_refresh(app):
    """
    Executa o scraping e, ao final, recarrega o DataFrame em memória.

    Usa o lock global para evitar concorrência.
    """
    lock: Lock = app.state.scrape_lock
    with lock:
        scraper.scrape_books()
        _reload_dataframe(app)

@router.post("/scraping/trigger")
def trigger_scraping(background_tasks: BackgroundTasks, request: Request):
    """
    Dispara o scraping em background.

    - Se já existir uma execução em andamento, retorna 409 (Conflict).
    - Caso contrário, agenda a tarefa e retorna imediatamente.

    Returns:
        dict|JSONResponse: Indicação de início ou conflito.
    """

    lock: Lock = request.app.state.scrape_lock
    if lock.locked():
        return JSONResponse(
            status_code=409,
            content={"started": False, "detail": "Scraper já está em execução."}
        )

    # agenda a execução em background
    background_tasks.add_task(_scrape_and_refresh, request.app)
    return {"started": True, "detail": "Scraper iniciado em background."}
