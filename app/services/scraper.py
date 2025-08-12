import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
import os
import csv
from app.utils.scraper_utilitys import EXISTING_TITLES, append_book_to_csv, get_rating

BASE_URL = "https://books.toscrape.com/catalogue/"
def scrape_books():
    books = []
    page_url = BASE_URL + "page-1.html"

    while page_url:
        print(f"Scraping: {page_url}")
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")

        articles = soup.select("article.product_pod")

        for article in articles:
            title = article.h3.a["title"]
            price = article.select_one(".price_color").text.strip().lstrip("£")
            availability = article.select_one(".availability").text.strip()
            rating_class = article.select_one("p.star-rating")["class"][1]
            rating = get_rating(rating_class)
            image_url = urljoin(BASE_URL, article.img["src"])

            book_relative_url = article.h3.a["href"]
            book_url = urljoin(BASE_URL, book_relative_url)
            book_response = requests.get(book_url)
            book_soup = BeautifulSoup(book_response.content, "html.parser")
            category = book_soup.select("ul.breadcrumb li")[-2].text.strip()
            title = book_soup.select('h1')[-1].text.strip()
            book_to_save = {
                "title": title,
                "price": float(price),
                "availability": availability,
                "rating": rating,
                "category": category,
                "image_url": image_url
            }
            print("saving book...")
            if not title in EXISTING_TITLES:
                append_book_to_csv(book_to_save)
            else:
                print(f'The book: {title} already exists on books.cvs')
            time.sleep(0.1)

        next_btn = soup.select_one("li.next > a")
        if next_btn:
            next_page = next_btn["href"]
            page_url = BASE_URL + f"{next_page}"
        else:
            page_url = None

    print(f"✅Scraping complete!")


if __name__ == "__main__":
    scrape_books()