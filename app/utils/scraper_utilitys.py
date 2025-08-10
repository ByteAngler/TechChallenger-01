import os, csv
def get_rating(text):
    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return ratings.get(text)

def append_book_to_csv(book_data, file_path="data/books.csv"):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=book_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(book_data)

def load_existing_titles(file_path="data/books.csv"):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, newline='', encoding="utf-8") as f:
        if csv.DictReader(f):
            reader = csv.DictReader(f)
            return set(row["title"] for row in reader)
        else:
            return set()

EXISTING_TITLES = load_existing_titles()