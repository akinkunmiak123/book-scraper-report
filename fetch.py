import requests

URL = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0 (learning project)"}

response = requests.get(URL, headers=headers, timeout=10)
response.raise_for_status()

print("Status code:", response.status_code)
print("Content type:", response.headers.get("Content-Type"))
print("Length of HTML:", len(response.text))
print()
print(response.text[:500])   # first 500 characters