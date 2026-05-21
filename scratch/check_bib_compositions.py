import urllib.request
import csv
import io
from collections import Counter

url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
print("Baixando base para verificar livros bíblicos e suas abreviações de composition...")

try:
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        
        f = io.StringIO(content)
        reader = csv.reader(f)
        header = next(reader)
        
        book_idx = header.index('book')
        path_idx = header.index('sentence_path')
        bib_idx = header.index('bib')
        composition_idx = header.index('composition')
        
        compositions = Counter()
        book_to_comp = {}
        for row in reader:
            if not row:
                continue
            if row[bib_idx] == "bib":
                book_val = row[book_idx]
                comp_val = row[composition_idx]
                path_val = row[path_idx]
                
                compositions[comp_val] += 1
                if comp_val not in book_to_comp:
                    book_to_comp[comp_val] = set()
                book_to_comp[comp_val].add(book_val)
                
        print("\nCompositions encontradas e contagens:")
        for k, v in compositions.most_common():
            books_list = list(book_to_comp[k])[:5]
            print(f"  Composition: {k} (total de chunks: {v}) | Scrolls associados: {books_list}")
            
except Exception as e:
    print(f"Erro: {e}")
