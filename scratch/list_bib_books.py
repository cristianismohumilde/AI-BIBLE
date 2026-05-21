import urllib.request
import csv
import io
from collections import Counter

url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
print("Baixando base para analisar livros e correspondências...")

try:
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        
        f = io.StringIO(content)
        reader = csv.reader(f)
        header = next(reader)
        
        book_idx = header.index('book')
        bib_idx = header.index('bib')
        comp_idx = header.index('composition')
        path_idx = header.index('sentence_path')
        
        all_bibs = {}
        for row in reader:
            if not row:
                continue
            if row[bib_idx] == "bib":
                b = row[book_idx]
                c = row[comp_idx]
                p = row[path_idx]
                
                if b not in all_bibs:
                    all_bibs[b] = {"comp": c, "count": 0, "sample_paths": []}
                all_bibs[b]["count"] += 1
                if len(all_bibs[b]["sample_paths"]) < 2:
                    all_bibs[b]["sample_paths"].append(p)
                    
        print(f"Total de pergaminhos bíblicos (unique 'book' values where bib == 'bib'): {len(all_bibs)}")
        print("\nOs primeiros 50 pergaminhos bíblicos:")
        for k, v in list(all_bibs.items())[:50]:
            print(f"  Scroll: {k} | Composition: {v['comp']} | Chunks: {v['count']} | Sample Paths: {v['sample_paths']}")
            
except Exception as e:
    print(f"Erro: {e}")
