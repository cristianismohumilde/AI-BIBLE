import requests
url = "https://www.sefaria.org/api/texts/Genesis.1?vhe=Miqra%20according%20to%20the%20Masorah"
r = requests.get(url).json()
print("Hebrew verses length:", len(r.get("he", [])))
if r.get("he"):
    print("First verse Hebrew:", r["he"][0])
