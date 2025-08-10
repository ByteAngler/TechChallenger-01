from fastapi import APIRouter, Request
import os

router = APIRouter()

@router.get("/health")
def health_check(request: Request):
    # 1 - API está rodando
    api_status = "Online!"

    # 2 - CSV existe
    csv_path = getattr(request.app.state, "csv_path", "data/books.csv")
    csv_exists = os.path.exists(csv_path)

    # 3 - CSV carregado e integridade básica
    df = getattr(request.app.state, "df", None)
    data_loaded = df is not None
    required_cols = ["title", "price", "availability", "rating", "category", "image_url"]
    has_required_cols = data_loaded and all(col in df.columns for col in required_cols)

    return {
        "api_status": api_status,
        "csv_exists": csv_exists,
        "data_loaded": data_loaded,
        "has_required_columns": has_required_cols,
    }
