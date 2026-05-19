import urllib.request
import json
import concurrent.futures

# We want to check all NT books first
nt_books = [
    "40-matthew", "41-mark", "42-luke", "43-john", "44-acts", "45-romans",
    "46-1-corinthians", "47-2-corinthians", "48-galatians", "49-ephesians",
    "50-philippians", "51-colossians", "52-1-thessalonians", "53-2-thessalonians",
    "54-1-timothy", "55-2-timothy", "56-titus", "57-philemon", "58-hebrews",
    "59-james", "60-1-peter", "61-2-peter", "62-1-john", "63-2-john",
    "64-3-john", "65-jude", "66-revelation"
]

def check_book(book):
    url = f"https://raw.githubusercontent.com/biniama/ethiopic-bible-data/main/data/new-testament/{book}.json"
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

print("Checking NT books in biniama...")
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(check_book, nt_books)
    for book, gez_v, total_v in results:
        print(f"{book}: {gez_v}/{total_v} Ge'ez verses")
