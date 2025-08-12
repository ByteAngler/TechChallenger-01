"""
Endpoints para consulta de categorias.

- GET /categories: retorna a lista de categorias únicas em ordem alfabética.
"""
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/categories", response_model=list[str])
def list_categories(request: Request):
    """
    Retorna a lista de categorias disponíveis no dataset.

    Returns:
        list[str]: Categorias únicas (ordenadas).
    """
    df = request.app.state.df
    return sorted(df["category"].dropna().unique().tolist())