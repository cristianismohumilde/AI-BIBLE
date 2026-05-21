import requests
import json

url = "https://api.getbible.net/v2/lxx/books.json"
r = requests.get(url).json()
print(json.dumps(r, indent=2, ensure_ascii=False))
