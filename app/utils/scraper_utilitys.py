"""
Utilidades de scraping.

Contém funções auxiliares para:
- Mapear 'rating' textual para número.
- Acrescentar um livro ao CSV (modo append, criando header se necessário).
- Carregar títulos existentes para evitar duplicações.
"""
import os, csv
def get_rating(text):
    """
    Converte o texto de rating em um inteiro (1-5).

    Args:
        text: Texto de rating vindo do HTML (ex.: "Three").

    Returns:
        int|None: Valor numérico do rating ou None se não mapeado.
    """
    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return ratings.get(text)

def append_book_to_csv(book_data, file_path="data/books.csv"):
    """
    Acrescenta uma linha (livro) ao CSV, criando o cabeçalho se ele não existir.

    Args:
        book_data: Dicionário com os campos do livro.
        file_path: Caminho do arquivo CSV.
    """
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=book_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(book_data)

def load_existing_titles(file_path="data/books.csv"):
    """
    Carrega os títulos existentes no CSV para evitar duplicações.

    Args:
        file_path: Caminho do arquivo CSV.

    Returns:
        set[str]: Conjunto de títulos já presentes no CSV.
    """
    if not os.path.exists(file_path):
        return set()
    with open(file_path, newline='', encoding="utf-8") as f:
        if csv.DictReader(f):
            reader = csv.DictReader(f)
            return set(row["title"] for row in reader)
        else:
            return set()

EXISTING_TITLES = load_existing_titles()