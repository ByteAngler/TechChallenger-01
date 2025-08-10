from fastapi import APIRouter, Depends, HTTPException, Query, Request
from app.models.book import Book

router = APIRouter(prefix="/books")

@router.get("/")
def get_df(request: Request):
    books = request.app.state.df.to_dict(orient="records")
    for b in books:
        b["id"] = int(b["id"])
        b["rating"] = int(b["rating"])
        b["price"] = float(b["price"])
    return {"titles": [b["title"] for b in books]}


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, request: Request):
    df = request.app.state.df
    row = df[df["id"] == book_id]
    if row.empty:
        raise HTTPException(404, "Book not found")
    return row.iloc[0].to_dict()

@router.get("/{book_id}", response_model=Book)
def get_book_by_title(book_id: int, request: Request):
    df = request.app.state.df
    row = df[df["id"] == book_id]
    if row.empty:
        raise HTTPException(404, "Book not found")
    return row.iloc[0].to_dict()

@router.get("/books/search", response_model=list[Book])
def search_books(
    request: Request,
    title: str | None = None,
    category: str | None = None,
):
    df = request.app.state.df
    if title:
        df = df[df["title"].str.contains(title, case=False, na=False)]
    if category:
        df = df[df["category"].str.contains(category, case=False, na=False)]
    return df.to_dict(orient="records")
    

