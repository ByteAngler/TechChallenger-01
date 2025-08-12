from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from threading import Lock
import pandas as pd

from app.services import scraper  # usa o seu scraper.py existente

router = APIRouter()

def _reload_dataframe(app) -> None:
    """Recarrega o CSV para a memória (app.state.df)."""
    csv_path = getattr(app.state, "csv_path", "data/books.csv")
    df = pd.read_csv(csv_path)

    if "id" not in df.columns:
        df = df.reset_index().rename(columns={"index": "id"})

    for col, cast in (("id", int), ("rating", int), ("price", float)):
        if col in df.columns:
            df[col] = df[col].apply(lambda x: None if pd.isna(x) else cast(x))

    app.state.df = df

def _scrape_and_refresh(app):
    """Executa o scraping e, ao final, recarrega o DF."""
    lock: Lock = app.state.scrape_lock
    with lock:
        scraper.scrape_books()   # usa sua lógica atual (com detecção de duplicatas)
        _reload_dataframe(app)

@router.post("/scraping/trigger")
def trigger_scraping(background_tasks: BackgroundTasks, request: Request):
    """
    Dispara o scraping em background. Se já estiver rodando, não dispara de novo.
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
