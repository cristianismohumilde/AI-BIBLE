import requests
import json

url = "https://query.getbible.net/v2/lxx/Genesis 1:1"
r = requests.get(url).json()
print(json.dumps(r, indent=2, ensure_ascii=False))
