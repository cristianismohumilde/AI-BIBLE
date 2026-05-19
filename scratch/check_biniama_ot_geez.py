import urllib.request
import json
import concurrent.futures

ot_books = [
    "01-genesis", "02-exodus", "03-leviticus", "04-numbers", "05-deuteronomy",
    "06-joshua", "07-judges", "08-ruth", "09-1-samuel", "10-2-samuel",
    "11-1-kings", "12-2-kings", "13-1-chronicles", "14-2-chronicles"
]

def check_book(book):
    url = f"https://raw.githubusercontent.com/biniama/ethiopic-bible-data/main/data/old-testament/{book}.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
            has_gez = False
            total_verses = 0
            gez_verses = 0
            for ch in data.get('chapters', []):
                for v in ch.get('verses', []):
                    total_verses += 1
                    if v.get('text', {}).get('gez') is not None:
                        gez_verses += 1
            return book, gez_verses, total_verses
    except Exception as e:
        return book, 0, 0

print("Checking OT books in biniama...")
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(check_book, ot_books)
    for book, gez_v, total_v in results:
        print(f"{book}: {gez_v}/{total_v} Ge'ez verses")
