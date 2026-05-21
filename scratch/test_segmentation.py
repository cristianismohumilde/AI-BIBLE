import urllib.request
import csv
import io
import json
import re

def strip_hebrew_diacritics(text):
    clean = re.sub(r'[\u0591-\u05C7]', '', text)
    clean = re.sub(r'[^\u05D0-\u05EA\s]', ' ', clean)
    return ' '.join(clean.split())

def word_similarity(w1, w2):
    # Check if words are identical or very similar (e.g. spelling variants)
    if w1 == w2:
        return 1.0
    # Qumran spelling variants often add 'yod' or 'waw' or 'aleph' at the end
    # Let's check if they share a common core
    if len(w1) > 2 and len(w2) > 2:
        # If one is a variant of another by adding/removing specific letters (א, י, ו, ה)
        set1 = set(w1) - {'א', 'י', 'ו', 'ה'}
        set2 = set(w2) - {'א', 'י', 'ו', 'ה'}
        if set1 == set2:
            return 0.8
    return 0.0

def align_chunk_to_verses(chunk_text, aleppo_verses):
    """
    Align a chunk of Qumran text to a list of Aleppo verses.
    aleppo_verses is a list of tuples: (verse_num, list_of_cleaned_words, raw_verse_text)
    Returns a dict mapping verse_num to list of Qumran words.
    """
    chunk_clean = strip_hebrew_diacritics(chunk_text)
    chunk_words = chunk_clean.split()
    raw_words = chunk_text.split() # raw words to preserve original orthography and brackets
    
    if len(chunk_words) != len(raw_words):
        # Fallback if cleaning changed word count (rare if we just split by space)
        raw_words = chunk_words
        
    # Step 1: Find the best window of verses for this chunk
    # We score each verse for total matching words
    verse_scores = []
    for idx, (v_num, v_words, _) in enumerate(aleppo_verses):
        matches = 0
        for qw in chunk_words:
            if any(word_similarity(qw, vw) > 0.7 for vw in v_words):
                matches += 1
        verse_scores.append((idx, matches))
        
    # Find the verse with the highest match to anchor the chunk
    verse_scores.sort(key=lambda x: x[1], reverse=True)
    best_idx = verse_scores[0][0]
    
    # We search in a local window around the best matching verse (e.g., 5 verses before and after)
    window_start = max(0, best_idx - 3)
    window_end = min(len(aleppo_verses), best_idx + 4)
    candidate_verses = aleppo_verses[window_start:window_end]
    
    # Step 2: Assign each word in the chunk to one of the candidate verses
    # We want a non-decreasing assignment sequence A_1, A_2, ..., A_N
    # We can use a simple dynamic programming to find the optimal assignment!
    # dp[i][j] = max score for aligning first i Qumran words to first j candidate verses
    # Let's define the score of aligning word i to candidate verse j:
    # similarity of word i to the best matching word in verse j
    
    N = len(chunk_words)
    M = len(candidate_verses)
    
    dp = [[-1e9] * M for _ in range(N)]
    parent = [[-1] * M for _ in range(N)]
    
    # Base case: first word
    for j in range(M):
        v_num, v_words, _ = candidate_verses[j]
        sim = max([word_similarity(chunk_words[0], vw) for vw in v_words] + [0.0])
        dp[0][j] = sim
        
    for i in range(1, N):
        for j in range(M):
            v_num, v_words, _ = candidate_verses[j]
            sim = max([word_similarity(chunk_words[i], vw) for vw in v_words] + [0.0])
            
            # We can transition from j (staying in the same verse) or j-1 (moving to the next verse)
            best_prev_score = dp[i-1][j]
            best_prev_j = j
            
            if j > 0 and dp[i-1][j-1] > best_prev_score:
                best_prev_score = dp[i-1][j-1]
                best_prev_j = j-1
                
            dp[i][j] = best_prev_score + sim
            parent[i][j] = best_prev_j
            
    # Backtrack to find the optimal verse assignment for each word
    assignments = []
    curr_j = M - 1 # start from the last candidate verse
    # find the best ending j
    best_end_score = -1e9
    for j in range(M):
        if dp[N-1][j] > best_end_score:
            best_end_score = dp[N-1][j]
            curr_j = j
            
    for i in range(N - 1, -1, -1):
        assignments.append(curr_j)
        curr_j = parent[i][curr_j]
    assignments.reverse()
    
    # Map assignments to verse numbers and group words
    verse_to_words = {}
    for i, j_idx in enumerate(assignments):
        v_num = candidate_verses[j_idx][0]
        if v_num not in verse_to_words:
            verse_to_words[v_num] = []
        verse_to_words[v_num].append(raw_words[i])
        
    return verse_to_words

def main():
    # Load Aleppo Isaiah 1
    aleppo_path = "/home/venelouis/Desktop/REPOS/AI-BIBLE/data/Aleppo/Isaiah/1.json"
    with open(aleppo_path, "r", encoding="utf-8") as f:
        aleppo_data = json.load(f)
        
    aleppo_verses = []
    for i, v_text in enumerate(aleppo_data["he"]):
        clean_v = strip_hebrew_diacritics(v_text)
        v_words = clean_v.split()
        aleppo_verses.append((i + 1, v_words, v_text))
        
    # Fetch first few chunks of 1Qisaa
    url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        f = io.StringIO(content)
        reader = csv.reader(f)
        header = next(reader)
        
        book_idx = header.index('book')
        bib_idx = header.index('bib')
        text_idx = header.index('text')
        path_idx = header.index('sentence_path')
        
        dss_chunks = []
        for row in reader:
            if not row:
                continue
            if row[bib_idx] == "bib" and row[book_idx] == "1Qisaa":
                dss_chunks.append((row[path_idx], row[text_idx]))
                if len(dss_chunks) >= 3:
                    break
                    
        for path, text in dss_chunks:
            print(f"\n--- Alinhando chunk {path} ---")
            aligned = align_chunk_to_verses(text, aleppo_verses)
            for v_num, words in sorted(aligned.items()):
                reconstructed = ' '.join(words)
                print(f"  Versículo {v_num} reconstruído:")
                print(f"    DSS   : {reconstructed[:150]}...")
                print(f"    Aleppo: {aleppo_data['he'][v_num-1][:150]}...")

if __name__ == "__main__":
    main()
