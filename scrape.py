import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0 (learning project)"}

response = requests.get(URL, headers=headers, timeout=10)
response.raise_for_status()
response.encoding = "utf-8"   # fixes the £ sign showing as Â£

soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")
print("Books found:", len(books))
print()

for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    rating = book.find("p", class_="star-rating")["class"][1]
    in_stock = book.find("p", class_="availability").text.strip()

    print(title, "|", price, "|", rating, "|", in_stock)