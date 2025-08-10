from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    price: float
    availability: str
    rating: int
    category: str
    image_url: str
