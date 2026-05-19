import json
import os

data_dir = "data/ancient_versions"
files = ["peshitta_syriac.json", "coptic_sahidic.json", "armenian_eastern.json"]

for f in files:
    fpath = os.path.join(data_dir, f)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as file:
            data = json.load(file)
            books = data.get("books", [])
            total_chapters = sum(len(b.get("chapters", [])) for b in books)
            print(f"{f}: {len(books)} books, {total_chapters} chapters")
    else:
        print(f"{f} not found")
