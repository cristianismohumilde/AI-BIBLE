import urllib.request
import csv
import io
from collections import Counter

url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
print("Baixando base para verificar mapeamento de livros bíblicos...")

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
        
        bib_books = {}
        for row in reader:
            if not row:
                continue
            if row[bib_idx] == "bib":
                book_val = row[book_idx]
                comp_val = row[composition_idx]
                path_val = row[path_idx]
                
                # Exemplo de chave: (book_val, comp_val)
                key = (book_val, comp_val)
                if key not in bib_books:
                    bib_books[key] = []
                if len(bib_books[key]) < 3:
                    bib_books[key].append(path_val)
                    
        print("\nAlgumas combinações de (book, composition) para textos bíblicos:")
        for key, paths in list(bib_books.items())[:30]:
            print(f"  Book: {key[0]} | Composition: {key[1]} | Exemplos de caminhos: {paths}")
            
except Exception as e:
    print(f"Erro: {e}")
