import urllib.request
import csv
import io

url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
print("Baixando amostra do 1Qisaa...")

try:
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        
        f = io.StringIO(content)
        reader = csv.reader(f)
        header = next(reader)
        
        book_col_idx = header.index('book')
        path_col_idx = header.index('sentence_path')
        text_col_idx = header.index('text')
        
        count = 0
        for row in reader:
            if not row:
                continue
            if row[book_col_idx] == "1Qisaa":
                print(f"\nChunk {count+1} ({row[path_col_idx]}):")
                print(row[text_col_idx][:300] + "...")
                count += 1
                if count >= 5:
                    break
except Exception as e:
    print(f"Erro: {e}")
