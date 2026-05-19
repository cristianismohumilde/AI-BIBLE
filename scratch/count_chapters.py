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

targum_chapters = 0
for f in sorted(os.listdir(data_dir)):
    if f.startswith("targum_onkelos") and f.endswith(".json"):
        fpath = os.path.join(data_dir, f)
        with open(fpath, "r", encoding="utf-8") as file:
            data = json.load(file)
            chapters = data.get("text", [])
            targum_chapters += len(chapters)
            print(f"{f}: {len(chapters)} chapters")
print(f"Total Targum: {targum_chapters} chapters")
