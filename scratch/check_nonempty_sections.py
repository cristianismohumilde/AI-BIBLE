import urllib.request
import csv
import io

url = "https://huggingface.co/datasets/yonatanlou/QumranDataset/resolve/main/dss_chunk_size_100_overlap_15.csv"
print("Baixando base para verificar registros bíblicos com section não vazia...")

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
        sect_idx = header.index('section')
        
        count = 0
        for row in reader:
            if not row:
                continue
            if row[bib_idx] == "bib" and row[sect_idx].strip() != "":
                print(f"Book: {row[book_idx]} | Composition: {row[comp_idx]} | Section: {row[sect_idx]} | Path: {row[path_idx]}")
                count += 1
                if count >= 30:
                    break
        if count == 0:
            print("Nenhum registro bíblico tem a coluna 'section' preenchida!")
            
except Exception as e:
    print(f"Erro: {e}")
