import logging
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import DATA_DIR, HEADERS, MAX_RETRIES, RETRY_WAIT_SECONDS, URL

logger = logging.getLogger(__name__)

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_html():
    """Download the page, retrying a few times if the network hiccups."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(URL, headers=HEADERS, timeout=10)
            response.raise_for_status()
            response.encoding = "utf-8"
            return response.text
        except requests.RequestException as error:
            logger.warning("Attempt %d/%d failed: %s", attempt, MAX_RETRIES, error)
            if attempt == MAX_RETRIES:
                raise
            time.sleep(RETRY_WAIT_SECONDS)


def scrape_books():
    soup = BeautifulSoup(fetch_html(), "html.parser")

    rows = []
    for book in soup.find_all("article", class_="product_pod"):
        rows.append({
            "title": book.h3.a["title"],
            "price": book.find("p", class_="price_color").text,
            "rating": book.find("p", class_="star-rating")["class"][1],
            "in_stock": book.find("p", class_="availability").text.strip(),
            "link": book.h3.a["href"],
        })

    if not rows:
        raise ValueError("No books found. The site layout may have changed.")

    return rows


def clean(rows):
    df = pd.DataFrame(rows)

    # "£51.77" -> 51.77 (a real number)
    df["price"] = df["price"].str.extract(r"(\d+\.\d+)").astype(float)

    # "Three" -> 3
    df["rating"] = df["rating"].map(RATING_MAP)

    # "In stock" -> True
    df["in_stock"] = df["in_stock"].str.contains("In stock")

    # when this row was scraped
    df["scraped_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return df


def save(df):
    DATA_DIR.mkdir(exist_ok=True)

    df.to_csv(DATA_DIR / "books_latest.csv", index=False)

    history_path = DATA_DIR / "books_history.csv"
    df.to_csv(history_path, mode="a", header=not history_path.exists(), index=False)


if __name__ == "__main__":
    rows = scrape_books()
    df = clean(rows)
    save(df)

    print(df.head())
    print()
    print(df.dtypes)
    print()
    print(df["price"].mean())
    print(df.sort_values("price").head(3))
    print(f"Saved {len(df)} books.")