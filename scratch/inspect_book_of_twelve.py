import urllib.request
import csv
import io

url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
print("Baixando base para verificar caminhos em 'Book of Twelve'...")

try:
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        
        f = io.StringIO(content)
        reader = csv.reader(f)
        header = next(reader)
        
        book_idx = header.index('book')
        path_idx = header.index('sentence_path')
        bib_idx = header.index('bib')
        comp_idx = header.index('composition')
        text_idx = header.index('text')
        
        count = 0
        for row in reader:
            if not row:
                continue
            if row[bib_idx] == "bib" and row[comp_idx] == "Book of Twelve":
                print(f"Book: {row[book_idx]} | Composition: {row[comp_idx]} | Path: {row[path_idx]} | Text: {row[text_idx][:100]}...")
                count += 1
                if count >= 20:
                    break
                    
except Exception as e:
    print(f"Erro: {e}")
