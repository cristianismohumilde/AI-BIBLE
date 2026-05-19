import json
import os

source_dir = "scratch/EthiopicBibleAPI/Books"
target_dir = "data/ancient_versions/geez_extracted"

os.makedirs(target_dir, exist_ok=True)

books_processed = 0
chapters_processed = 0

for f in os.listdir(source_dir):
    if f.endswith(".json"):
        with open(os.path.join(source_dir, f), "r", encoding="utf-8") as file:
            data = json.load(file)
            
            if isinstance(data, dict) and "chapters" in data:
                book_name = data.get("title", f.replace(".json", "")).strip()
                books_processed += 1
                
                for chapter_data in data["chapters"]:
                    ch_num = chapter_data.get("chapter")
                    verses = chapter_data.get("verses", [])
                    
                    if ch_num and verses:
                        verse_texts = []
                        # No Amharic/Ge'ez do EthiopicBibleAPI, verses é uma lista de strings
                        for i, v_text in enumerate(verses):
                            if v_text.strip() and v_text != "-":
                                verse_texts.append(f"{i + 1} {v_text}")
                        
                        if verse_texts:
                            output_file = os.path.join(target_dir, f"{book_name}_{ch_num}.json")
                            with open(output_file, "w", encoding="utf-8") as out_f:
                                json.dump({"text": verse_texts}, out_f, ensure_ascii=False, indent=2)
                            chapters_processed += 1

print(f"Ge'ez extraction complete: {books_processed} books, {chapters_processed} chapters extracted to {target_dir}")
