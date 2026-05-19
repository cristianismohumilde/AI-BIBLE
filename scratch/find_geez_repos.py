import urllib.request
import json

queries = ["geez-bible", "geez_bible", "ethiopic-bible", "ethiopic_bible", "geez-new-testament", "ethiopic-new-testament"]
for q in queries:
    url = f"https://api.github.com/search/repositories?q={q}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
            items = data.get('items', [])
            if items:
                print(f"=== Query: {q} ===")
                for item in items[:5]:
                    print(f"  {item['full_name']} - {item['description']}")
    except Exception as e:
        print(f"Query {q} failed: {e}")
