import json
import re
import os
from collections import defaultdict

BOOK_MAP = {
    "Genesis": "GEN", "Exodus": "EXO", "Leviticus": "LEV", "Numbers": "NUM", "Deuteronomy": "DEU",
    "Joshua": "JOS", "Judges": "JDG", "Ruth": "RUT", "1_Samuel": "1SA", "2_Samuel": "2SA",
    "1_Kings": "1KI", "2_Kings": "2KI", "1_Chronicles": "1CH", "2_Chronicles": "2CH",
    "Ezra": "EZR", "Nehemiah": "NEH", "Esther": "EST", "Job": "JOB", "Psalms": "PSA",
    "Proverbs": "PRO", "Ecclesiastes": "ECC", "Song_of_Solomon": "SNG", "Isaiah": "ISA",
    "Jeremiah": "JER", "Lamentations": "LAM", "Ezekiel": "EZK", "Daniel": "DAN",
    "Hosea": "HOS", "Joel": "JOL", "Amos": "AMO", "Obadiah": "OBA", "Jonah": "JON",
    "Micah": "MIC", "Nahum": "NAM", "Habakkuk": "HAB", "Zephaniah": "ZEP",
    "Haggai": "HAG", "Zechariah": "ZEC", "Malachi": "MAL"
}

def load_macula():
    print("Loading Macula Hebrew TSV...")
    mapping = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    
    with open("data/study_materials/macula-hebrew.tsv", "r", encoding="utf-8") as f:
        header = f.readline().strip().split('\t')
        try:
            ref_idx = header.index("ref")
            strongs_idx = header.index("strongnumberx")
        except ValueError:
            print("TSV format unexpected!")
            return mapping

        for line in f:
            parts = line.strip('\n').split('\t')
            if len(parts) <= max(ref_idx, strongs_idx):
                continue
                
            ref = parts[ref_idx]
            strong_raw = parts[strongs_idx]
            
            if not ref or "!" not in ref:
                continue
                
            # ref looks like: GEN 1:1!1
            try:
                book_cv, word_num = ref.split('!')
                book, cv = book_cv.split(' ', 1)
                chapter, verse = cv.split(':')
                word_num = int(word_num)
            except Exception:
                continue
            
            # Format strongs
            if strong_raw:
                # remove letters a, b, c etc from the end
                strong_clean = re.sub(r'[a-zA-Z]+$', '', strong_raw)
                # strip leading zeros
                try:
                    strong_clean = str(int(strong_clean))
                    strong_id = f"H{strong_clean}"
                    # We overwrite with the latest morph strong's ID (which is usually the root)
                    mapping[book][int(chapter)][int(verse)][word_num] = strong_id
                except ValueError:
                    pass
                    
    return mapping

def process_all(mapping):
    output_dir = "output/Aleppo"
    if not os.path.exists(output_dir):
        print("output/Aleppo not found!")
        return

    total_files = 0
    total_verses = 0
    injected_verses = 0

    # Punctuation to separate words from but NOT count as word delimiters
    # In Hebrew, sof pasuq (׃) or colon/comma are attached to words. 
    # We only split by space and maqaf (־)
    for file_name in os.listdir(output_dir):
        if not file_name.endswith(".json"):
            continue
            
        # Parse book and chapter from filename
        # e.g. 1_Kings_22.json
        parts = file_name.replace(".json", "").split("_")
        chapter_str = parts[-1]
        book_name = "_".join(parts[:-1])
        
        try:
            chapter = int(chapter_str)
        except ValueError:
            continue
            
        book_abbr = BOOK_MAP.get(book_name)
        if not book_abbr:
            continue

        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                continue

        modified = False
        
        for verse_obj in data:
            verse = verse_obj.get("verse")
            original = verse_obj.get("original", "")
            if not verse or not original:
                continue
                
            total_verses += 1
            
            # Remove any existing strongs tags if we are reprocessing
            original_clean = re.sub(r'<span data-strong=".*?">(.*?)</span>', r'\1', original)
            
            # Split by space and maqaf
            tokens = re.split(r'([\s־]+)', original_clean)
            
            # The actual words are at even indices
            words = [tokens[i] for i in range(0, len(tokens), 2) if tokens[i]]
            
            macula_words = mapping[book_abbr][chapter].get(int(verse), {})
            
            # Check length alignment
            if len(words) == len(macula_words):
                new_tokens = list(tokens)
                word_idx = 1
                for i in range(0, len(new_tokens), 2):
                    if not new_tokens[i]:
                        continue
                    
                    # Extract the word, ignoring punctuation attached to the end (like sof pasuq ׃)
                    word_str = new_tokens[i]
                    
                    strong_id = macula_words.get(word_idx)
                    if strong_id:
                        # Wrap the word, keeping any punctuation inside or outside?
                        # It's fine to wrap the punctuation inside the span.
                        new_tokens[i] = f'<span data-strong="{strong_id}">{word_str}</span>'
                        
                    word_idx += 1
                    
                verse_obj["original"] = "".join(new_tokens)
                injected_verses += 1
                modified = True
            else:
                # Length mismatch, skip
                pass

        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            total_files += 1

    print(f"Processed {total_files} files.")
    print(f"Injected Strong's into {injected_verses} out of {total_verses} verses.")

if __name__ == "__main__":
    mapping = load_macula()
    process_all(mapping)
