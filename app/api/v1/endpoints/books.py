"""
Endpoints para consulta de livros.

Rotas atuais:
- GET /books/           -> retorna apenas uma lista com os títulos (comportamento atual do projeto)
- GET /books/{book_id}  -> retorna um livro por ID
- GET /books/books/search -> busca por título e/ou categoria (sem paginação)
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from app.models.book import Book

router = APIRouter(prefix="/books")

@router.get("/")
def get_df(request: Request):
    """
    Retorna todos os livros carregados (comportamento atual retorna apenas lista de títulos).

    Obs.: Se desejar retornar os registros completos, trocar o retorno para o DataFrame convertido.
    """
    books = request.app.state.df.to_dict(orient="records")
    for b in books:
        b["id"] = int(b["id"])
        b["rating"] = int(b["rating"])
        b["price"] = float(b["price"])
    return {"titles": [b["title"] for b in books]}


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, request: Request):
    """
    Retorna um livro específico pelo ID.

    Args:
        book_id: Identificador interno do livro.

    Raises:
        HTTPException(404): Se o ID não existir.
    """
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
    """
    Busca livros por título e/ou categoria (sem paginação).

    Args:
        title: Trecho do título para busca (case-insensitive).
        category: Trecho da categoria para busca (case-insensitive).

    Returns:
        list[Book]: Lista de livros que atendem aos filtros.
    """
    df = request.app.state.df
    if title:
        df = df[df["title"].str.contains(title, case=False, na=False)]
    if category:
        df = df[df["category"].str.contains(category, case=False, na=False)]
    return df.to_dict(orient="records")
    

