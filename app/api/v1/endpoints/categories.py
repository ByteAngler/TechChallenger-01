from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/categories", response_model=list[str])
def list_categories(request: Request):
    df = request.app.state.df
    return sorted(df["category"].dropna().unique().tolist())