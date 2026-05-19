import json
import os

data_dir = "data/Talmud"
total_pages = 0
books = 0

for f in os.listdir(data_dir):
    if f.endswith(".json"):
        books += 1
        with open(os.path.join(data_dir, f), "r", encoding="utf-8") as file:
            data = json.load(file)
            pages = data.get("text", [])
            # We count non-empty pages just like translate_bible.py does
            valid_pages = sum(1 for p in pages if p and isinstance(p, list) and len(p) > 0)
            total_pages += valid_pages

print(f"Talmud: {books} tractates, {total_pages} valid pages/amudim")
