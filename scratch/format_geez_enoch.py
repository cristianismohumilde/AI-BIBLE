import os
import json

geez_extracted_dir = "data/ancient_versions/geez_extracted"
os.makedirs(geez_extracted_dir, exist_ok=True)

enoch_path = "data/ancient_versions/enoch_geez.json"
try:
    with open(enoch_path, "r", encoding="utf-8") as f:
        enoch_data = json.load(f)
    
    saved_chapters = 0
    for ch_num, ch_data in enoch_data.items():
        verses = ch_data.get("verses", {})
        if not verses:
            continue
        
        # Format: ["1 verse1", "2 verse2", ...]
        formatted_verses = []
        for v_num in sorted(verses.keys(), key=lambda x: int(x)):
            v_data = verses[v_num]
            v_geez = v_data.get("geez", "").strip()
            if v_geez:
                formatted_verses.append(f"{v_num} {v_geez}")
        
        if formatted_verses:
            # Name format: መጽሐፈ ሄኖክ_1.json
            out_file = os.path.join(geez_extracted_dir, f"መጽሐፈ ሄኖክ_{ch_num}.json")
            with open(out_file, "w", encoding="utf-8") as out_f:
                json.dump({"text": formatted_verses}, out_f, ensure_ascii=False, indent=2)
            saved_chapters += 1
            
    print(f"Success! Formatted and saved {saved_chapters} chapters of Classical Ge'ez Enoch.")
except Exception as e:
    print("Error formatting Ge'ez Enoch:", e)
