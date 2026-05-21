import os
import json
import csv
import io
import re
import urllib.request

# --- Configurations and Mappings ---
ALEPPO_DIR = "/home/venelouis/Desktop/REPOS/AI-BIBLE/data/Aleppo"
DSS_DIR = "/home/venelouis/Desktop/REPOS/AI-BIBLE/data/DSS"
QUMRAN_URL = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"

COMPOSITION_TO_BOOKS = {
    "Gen": ["Genesis"],
    "Ex": ["Exodus"],
    "Lev": ["Leviticus"],
    "Num": ["Numbers"],
    "Deut": ["Deuteronomy"],
    "Josh": ["Joshua"],
    "Judg": ["Judges"],
    "Samuel": ["1_Samuel", "2_Samuel"],
    "Kings": ["1_Kings", "2_Kings"],
    "Is": ["Isaiah"],
    "Jer": ["Jeremiah"],
    "Ezek": ["Ezekiel"],
    "Ps": ["Psalms"],
    "Job": ["Job"],
    "Prov": ["Proverbs"],
    "Ruth": ["Ruth"],
    "Song": ["Song_of_Solomon"],
    "Eccl": ["Ecclesiastes"],
    "Lam": ["Lamentations"],
    "Esther": ["Esther"],
    "Dan": ["Daniel"],
    "Ezra": ["Ezra", "Nehemiah"],
    "1Chr": ["1_Chronicles", "2_Chronicles"],
    "2Chr": ["1_Chronicles", "2_Chronicles"],
    "Book of Twelve": ["Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"]
}

SCROLL_EXPLICIT_MAP = {
    "Mur1": "Gen",
    "Mur2": "Deut",
    "Mur3": "Is",
    "Mur4": "Ex",
    "Mur88": "Book of Twelve",
    "Murx": "Gen",
    "Sdeir1": "Gen",
    "5/6hev1a": "Num",
    "5/6hev1b": "Ps",
    "Xhev/se2": "Num",
    "Xhev/se3": "Deut",
    "Xhev/se5": "Ex",
    "34Se1": "Ex",
    "Mas1": "Gen",
    "Mas1a": "Lev",
    "Mas1b": "Lev",
    "Mas1c": "Deut",
    "Mas1d": "Ezek",
    "Mas1e": "Ps",
    "Mas1f": "Ps",
    "Arugleviticus": "Lev",
    "Xjoshua": "Josh",
    "Xjudges": "Judg"
}

def strip_hebrew_diacritics(text):
    # Strip vowels, cantillation marks, and non-Hebrew letters
    clean = re.sub(r'[\u0591-\u05C7]', '', text)
    clean = re.sub(r'[^\u05D0-\u05EA\s]', ' ', clean)
    return ' '.join(clean.split())

def word_similarity(w1, w2):
    if w1 == w2:
        return 1.0
    if len(w1) > 2 and len(w2) > 2:
        # Check similarity ignoring typical Second Temple spelling variants (waw/yod/aleph/he)
        set1 = set(w1) - {'א', 'י', 'ו', 'ה'}
        set2 = set(w2) - {'א', 'י', 'ו', 'ה'}
        if set1 == set2:
            return 0.8
    return 0.0

def load_aleppo_codex():
    """Load and index all Aleppo Codex reference texts in memory."""
    print("Carregando Códice de Aleppo como referência para alinhamento...")
    aleppo_db = {} # book -> list of (chapter, verse_num, clean_words, raw_text)
    
    for book in os.listdir(ALEPPO_DIR):
        book_path = os.path.join(ALEPPO_DIR, book)
        if not os.path.isdir(book_path):
            continue
            
        aleppo_db[book] = []
        for ch_file in os.listdir(book_path):
            if not ch_file.endswith(".json"):
                continue
            ch_num = int(ch_file.split(".")[0])
            
            with open(os.path.join(book_path, ch_file), "r", encoding="utf-8") as f:
                data = json.load(f)
                
            for idx, text in enumerate(data.get("he", [])):
                v_num = idx + 1
                clean_v = strip_hebrew_diacritics(text)
                v_words = clean_v.split()
                aleppo_db[book].append((ch_num, v_num, v_words, text))
                
        # Sort by chapter and verse to ensure sequential list
        aleppo_db[book].sort(key=lambda x: (x[0], x[1]))
        
    print(f"Códice de Aleppo carregado. Total de livros catalogados: {len(aleppo_db)}.")
    return aleppo_db

def get_candidate_books(scroll_name, composition):
    """Determine candidate books for a given scroll chunk based on mappings."""
    if composition in COMPOSITION_TO_BOOKS:
        return COMPOSITION_TO_BOOKS[composition]
        
    # Check explicit scroll mapping
    if scroll_name in SCROLL_EXPLICIT_MAP:
        comp = SCROLL_EXPLICIT_MAP[scroll_name]
        return COMPOSITION_TO_BOOKS[comp]
        
    # Check name heuristics
    s_lower = scroll_name.lower()
    if "isa" in s_lower:
        return ["Isaiah"]
    if "deut" in s_lower:
        return ["Deuteronomy"]
    if "ex" in s_lower:
        return ["Exodus"]
    if "ps" in s_lower:
        return ["Psalms"]
    if "sam" in s_lower:
        return ["1_Samuel", "2_Samuel"]
    if "lev" in s_lower:
        return ["Leviticus"]
    if "num" in s_lower:
        return ["Numbers"]
    if "gen" in s_lower:
        return ["Genesis"]
    if "jer" in s_lower:
        return ["Jeremiah"]
    if "dan" in s_lower:
        return ["Daniel"]
    if "kings" in s_lower:
        return ["1_Kings", "2_Kings"]
    if "ezek" in s_lower:
        return ["Ezekiel"]
    if "josh" in s_lower:
        return ["Joshua"]
    if "judg" in s_lower:
        return ["Judges"]
    if "lam" in s_lower:
        return ["Lamentations"]
    if "song" in s_lower:
        return ["Song_of_Solomon"]
    if "job" in s_lower:
        return ["Job"]
    if "ruth" in s_lower:
        return ["Ruth"]
    if "eccl" in s_lower:
        return ["Ecclesiastes"]
    if "prov" in s_lower:
        return ["Proverbs"]
    if "ezra" in s_lower:
        return ["Ezra", "Nehemiah"]
    if "chr" in s_lower:
        return ["1_Chronicles", "2_Chronicles"]
        
    # Fallback: search all books
    return None

def align_chunk(chunk_text, candidate_verses):
    """Perform dynamic programming segmentation of Qumran chunk into candidate verses."""
    raw_words = chunk_text.split()
    chunk_words = [strip_hebrew_diacritics(w) for w in raw_words]
    
    N = len(chunk_words)
    M = len(candidate_verses)
    if N == 0 or M == 0:
        return {}
        
    # DP Table: dp[i][j] stores the best match score for first i Qumran words mapped to first j verses
    dp = [[-1e9] * M for _ in range(N)]
    parent = [[-1] * M for _ in range(N)]
    
    # Initialize base case (first word)
    for j in range(M):
        _, _, v_words, _ = candidate_verses[j]
        sim = max([word_similarity(chunk_words[0], vw) for vw in v_words] + [0.0])
        dp[0][j] = sim
        
    # Fill DP table
    for i in range(1, N):
        for j in range(M):
            _, _, v_words, _ = candidate_verses[j]
            sim = max([word_similarity(chunk_words[i], vw) for vw in v_words] + [0.0])
            
            # Transition from j (same verse) or j-1 (next verse)
            best_score = dp[i-1][j]
            best_prev_j = j
            
            if j > 0 and dp[i-1][j-1] > best_score:
                best_score = dp[i-1][j-1]
                best_prev_j = j-1
                
            dp[i][j] = best_score + sim
            parent[i][j] = best_prev_j
            
    # Backtrack to find optimal verse assignment
    best_end_score = -1e9
    curr_j = M - 1
    for j in range(M):
        if dp[N-1][j] > best_end_score:
            best_end_score = dp[N-1][j]
            curr_j = j
            
    assignments = []
    for i in range(N - 1, -1, -1):
        assignments.append(curr_j)
        curr_j = parent[i][curr_j]
    assignments.reverse()
    
    # Group raw words by assigned verse coordinates
    verse_groups = {}
    for i, j_idx in enumerate(assignments):
        ch, v_num, _, _ = candidate_verses[j_idx]
        key = (ch, v_num)
        if key not in verse_groups:
            verse_groups[key] = []
        verse_groups[key].append(raw_words[i])
        
    return verse_groups

def main():
    aleppo_db = load_aleppo_codex()
    
    # Download Qumran dataset
    print(f"Baixando base do QumranDataset de {QUMRAN_URL}...")
    try:
        with urllib.request.urlopen(QUMRAN_URL) as response:
            content = response.read().decode("utf-8")
    except Exception as e:
        print(f"Erro ao baixar dataset: {e}")
        return
        
    f = io.StringIO(content)
    reader = csv.reader(f)
    header = next(reader)
    
    book_idx = header.index('book')
    bib_idx = header.index('bib')
    comp_idx = header.index('composition')
    text_idx = header.index('text')
    path_idx = header.index('sentence_path')
    
    print("Processando chunks bíblicos do Mar Morto...")
    
    reconstructed_verses = {} # book -> chapter -> verse_num -> (text, match_count)
    
    chunk_count = 0
    matched_count = 0
    
    for row in reader:
        if not row:
            continue
        if row[bib_idx] != "bib":
            continue
            
        scroll_name = row[book_idx]
        composition = row[comp_idx]
        chunk_text = row[text_idx]
        chunk_path = row[path_idx]
        
        chunk_count += 1
        
        # Determine candidate books
        candidate_books = get_candidate_books(scroll_name, composition)
        if not candidate_books:
            # Fallback to all loaded books
            candidate_books = list(aleppo_db.keys())
            
        # Collect all reference verses across all candidate books
        ref_verses = []
        for b in candidate_books:
            if b in aleppo_db:
                for ch, v_num, v_words, raw_t in aleppo_db[b]:
                    ref_verses.append((b, ch, v_num, v_words, raw_t))
                    
        if not ref_verses:
            continue
            
        # Clean chunk words for scoring
        clean_chunk = strip_hebrew_diacritics(chunk_text)
        chunk_words = clean_chunk.split()
        
        # Score each reference verse
        best_ref_idx = -1
        best_score = -1
        for idx, (b, ch, v_num, v_words, _) in enumerate(ref_verses):
            score = 0
            for qw in chunk_words:
                if any(word_similarity(qw, vw) > 0.7 for vw in v_words):
                    score += 1
            if score > best_score:
                best_score = score
                best_ref_idx = idx
                
        # We require a minimal score (e.g. at least 3 matching words) to align safely
        if best_ref_idx == -1 or best_score < 3:
            continue
            
        matched_count += 1
        
        # The best matching verse anchors the chunk to a specific book
        best_book, best_ch, best_v, _, _ = ref_verses[best_ref_idx]
        
        # Filter reference verses to only those belonging to the anchored book
        book_verses = [(ch, v, vw, t) for b, ch, v, vw, t in ref_verses if b == best_book]
        
        # Find the index of the best matching verse within this book's verse list
        book_best_idx = next(i for i, (ch, v, _, _) in enumerate(book_verses) if ch == best_ch and v == best_v)
        
        # Narrow DP candidate window to 5 verses before and 6 verses after (total 12 verses)
        win_start = max(0, book_best_idx - 5)
        win_end = min(len(book_verses), book_best_idx + 7)
        candidate_window = book_verses[win_start:win_end]
        
        # Run alignment within this window
        aligned = align_chunk(chunk_text, candidate_window)
        
        # Store results
        if best_book not in reconstructed_verses:
            reconstructed_verses[best_book] = {}
            
        for (ch, v_num), words in aligned.items():
            reconstructed_text = ' '.join(words)
            clean_rec = strip_hebrew_diacritics(reconstructed_text)
            rec_words = clean_rec.split()
            
            # Find matching words count as quality metric
            ref_v_words = next(vw for ch_n, v_n, vw, _ in book_verses if ch_n == ch and v_n == v_num)
            match_score = sum(1 for rw in rec_words if any(word_similarity(rw, vw) > 0.7 for vw in ref_v_words))
            
            if ch not in reconstructed_verses[best_book]:
                reconstructed_verses[best_book][ch] = {}
                
            # If we already have a reconstruction for this verse, keep the one with higher match score
            if v_num in reconstructed_verses[best_book][ch]:
                prev_text, prev_score = reconstructed_verses[best_book][ch][v_num]
                if match_score > prev_score:
                    reconstructed_verses[best_book][ch][v_num] = (reconstructed_text, match_score)
            else:
                reconstructed_verses[best_book][ch][v_num] = (reconstructed_text, match_score)
                
    print(f"\nAlinhamento completo! Chunks processados: {chunk_count} | Alinhados com sucesso: {matched_count} ({(matched_count/chunk_count)*100:.1f}%).")
    
    # --- Write output back to Sefaria DSS Templates ---
    print("\nSalvando os versículos alinhados nos arquivos JSON em data/DSS/...")
    
    updated_files_count = 0
    updated_verses_count = 0
    
    for book, chapters in reconstructed_verses.items():
        book_dir = os.path.join(DSS_DIR, book)
        if not os.path.exists(book_dir):
            # Create if directory is missing for some reason
            os.makedirs(book_dir, exist_ok=True)
            
        for ch, verses in chapters.items():
            file_path = os.path.join(book_dir, f"{ch}.json")
            
            # Load template file or initialize if missing
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                # If file doesn't exist, let's create a template
                max_v = max(verses.keys())
                data = {
                    "ref": f"{book} {ch}",
                    "heRef": "",
                    "isComplex": False,
                    "text": [""] * max_v,
                    "he": [""] * max_v
                }
                
            # Ensure "he" array is present and is resized to match "text" array
            if "he" not in data or not isinstance(data["he"], list):
                data["he"] = []
                
            text_len = len(data.get("text", []))
            if len(data["he"]) < text_len:
                data["he"].extend([""] * (text_len - len(data["he"])))
                
            # Populate "he" array
            for v_num, (text, _) in verses.items():
                idx = v_num - 1
                # Check bounds
                if idx >= len(data["he"]):
                    # Extend array if needed
                    data["he"].extend([""] * (idx + 1 - len(data["he"])))
                    # Also extend text array to match
                    if "text" in data and isinstance(data["text"], list):
                        data["text"].extend([""] * (idx + 1 - len(data["text"])))
                        
                data["he"][idx] = text
                updated_verses_count += 1
                
            # Save updated JSON file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            updated_files_count += 1
            
    print(f"Salvo com sucesso! Total de capítulos/arquivos JSON atualizados: {updated_files_count}.")
    print(f"Total de versículos em Hebraico/Aramaico do Mar Morto restaurados: {updated_verses_count}.")

if __name__ == "__main__":
    main()
