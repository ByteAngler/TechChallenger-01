from fastapi import FastAPI
from app.api.v1.endpoints import books, categories, health
from fastapi.responses import RedirectResponse
import pandas as pd
from app.core.config import get_settings

app = FastAPI(title="Book API", version="1.0.0")
settings = get_settings()

@app.on_event("startup")
def load_data():
    df = pd.read_csv(settings.csv_path)
    print(df.shape)
    if "id" not in df.columns:
        df = df.reset_index().rename(columns={"index": "id"})
    app.state.df = df

@app.get("/")
def home():
    return RedirectResponse(url="/api/v1/health")

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(books.router,  prefix="/api/v1", tags=["Books"])
app.include_router(categories.router, prefix="/api/v1", tags=["Categories"])
