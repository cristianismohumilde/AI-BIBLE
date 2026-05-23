import requests
urls = [
    "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/CopSahBible2.json",
    "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/ArmEastern.json",
    "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/Peshitta.json",
    "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/syr.json",
    "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/gez.json"
]
for url in urls:
    try:
        r = requests.head(url, timeout=5)
        print(f"URL: {url}, Status: {r.status_code}")
    except Exception as e:
        print(f"URL: {url}, Exception: {e}")
