"""
Modelos Pydantic usados como contrato de resposta/entrada na API.
"""

from pydantic import BaseModel

class Book(BaseModel):
    """
    Representa um livro exposto pela API.

    Attributes:
        id: Identificador interno gerado na carga do CSV.
        title: Título do livro.
        price: Preço (float).
        availability: Status de disponibilidade textual.
        rating: Avaliação numérica (1-5).
        category: Categoria do livro.
        image_url: URL absoluta da imagem do livro.
    """
    id: int
    title: str
    price: float
    availability: str
    rating: int
    category: str
    image_url: str
