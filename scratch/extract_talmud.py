import os
import json

def main():
    talmud_dir = "data/Talmud"
    tractates = {}
    
    if os.path.isdir(talmud_dir):
        for f in os.listdir(talmud_dir):
            if f.endswith(".json"):
                name = f.replace(".json", "")
                fpath = os.path.join(talmud_dir, f)
                try:
                    with open(fpath, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        pages = data.get("text", [])
                        page_names = []
                        for i, page in enumerate(pages):
                            if page and isinstance(page, list) and len(page) > 0:
                                daf_num = i // 2 + 2
                                daf_side = "a" if i % 2 == 0 else "b"
                                page_names.append(f"{daf_num}{daf_side}")
                        if page_names:
                            tractates[name] = page_names
                except Exception as e:
                    print(f"Error reading {f}: {e}")
                    
    with open("scratch/talmud_structure.json", "w", encoding="utf-8") as out:
        json.dump(tractates, out, ensure_ascii=False, indent=2)
    print("Talmud structure extracted!")

if __name__ == "__main__":
    main()
