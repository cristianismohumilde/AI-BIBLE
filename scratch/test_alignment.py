import urllib.request
import csv
import io
import json
import re

def strip_hebrew_diacritics(text):
    # Strip vowels (nikkud), cantillation marks, and other diacritics
    # Hebrew vowels are in range \u05B0-\u05C4
    clean = re.sub(r'[\u0591-\u05C7]', '', text)
    # Remove punctuation and special characters
    clean = re.sub(r'[^\u05D0-\u05EA\s]', ' ', clean)
    return ' '.join(clean.split())

def main():
    # 1. Load Aleppo Isaiah 1
    aleppo_path = "/home/venelouis/Desktop/REPOS/AI-BIBLE/data/Aleppo/Isaiah/1.json"
    with open(aleppo_path, "r", encoding="utf-8") as f:
        aleppo_data = json.load(f)
    
    aleppo_verses = []
    for i, v_text in enumerate(aleppo_data["he"]):
        clean_v = strip_hebrew_diacritics(v_text)
        v_words = clean_v.split()
        aleppo_verses.append((i + 1, v_words, v_text))
        
    print(f"Carregados {len(aleppo_verses)} versículos de Aleppo Isaías 1.")

    # 2. Load Hugging Face QumranDataset
    url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
    print("Baixando base do QumranDataset para testar alinhamento...")
    
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
            
            f = io.StringIO(content)
            reader = csv.reader(f)
            header = next(reader)
            
            book_idx = header.index('book')
            path_idx = header.index('sentence_path')
            bib_idx = header.index('bib')
            text_idx = header.index('text')
            
            dss_chunks = []
            for row in reader:
                if not row:
                    continue
                if row[bib_idx] == "bib" and row[book_idx] == "1Qisaa":
                    dss_chunks.append((row[path_idx], row[text_idx]))
                    
            print(f"Carregados {len(dss_chunks)} chunks do 1Qisaa.")
            
            # 3. Test alignment for the first chunk
            chunk_path, chunk_text = dss_chunks[0]
            clean_chunk = strip_hebrew_diacritics(chunk_text)
            chunk_words = clean_chunk.split()
            
            print(f"\nTestando alinhamento para o primeiro chunk ({chunk_path}):")
            print(f"Texto do chunk: {chunk_text[:150]}...")
            
            # Find which verses in Aleppo Isaiah 1 match the words in this chunk
            verse_matches = []
            for v_num, v_words, raw_v in aleppo_verses:
                # Count matching words (exact consonant match)
                matches = 0
                for w in chunk_words:
                    if w in v_words:
                        matches += 1
                match_pct = (matches / len(v_words)) * 100 if v_words else 0
                verse_matches.append((v_num, matches, match_pct, raw_v))
                
            # Sort by number of matches
            verse_matches.sort(key=lambda x: x[1], reverse=True)
            print("\nMelhores correspondências de versículos:")
            for v_num, matches, pct, raw_v in verse_matches[:5]:
                print(f"  Versículo {v_num}: {matches} palavras batem ({pct:.1f}%) | Original: {raw_v[:80]}...")
                
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
